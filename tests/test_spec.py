
from io import BytesIO
from pymarc import Record, Field
from tempfile import TemporaryFile, NamedTemporaryFile
import unittest

from marc2iiif import IIIFDataExtractionFromMarc, IIIFMetadataBoxFromMarc, IIIFMetadataField

class Tests(unittest.TestCase):
    def testBuildIIIFDataExtractionFromMarc(self):
        metadata_box = IIIFMetadataBoxFromMarc('a label',
                                               'a description',
                                               '/foo/bar', [
                                                  IIIFMetadataField("a field", "a value")
                                             ])
        new_object = IIIFDataExtractionFromMarc(metadata_box)
        self.assertEqual(new_object.show_title(), 'a label')
        self.assertEqual(new_object.show_description(), 'a description')

    def testBuildIIIFMetadataBoxFromMarc(self):
        new_object = IIIFMetadataBoxFromMarc('a label',
                                             'a description',
                                             '/foo/bar', [
                                                 IIIFMetadataField("a field", "a value")
                                             ])
        self.assertEqual(new_object.label, 'a label')
        self.assertEqual(new_object.description, 'a description')
        self.assertEqual(new_object.identifier, '/foo/bar')

    def testBuildIIIFMetadataField(self):
        new_object = IIIFMetadataField("a field", "a value")
        self.assertEqual(new_object.label, 'a field')
        self.assertEqual(new_object.value, 'a value')

    def testLoadFromDict(self):
        test = {}
        test['fields'] = [
            {'245': {'ind1': '0',
                     'ind2': '0',
                     'subfields': [
                         {'a': 'A Title of a CHO'},
                         {'h': 'electronic resource'},
                         {'c': 'Doe, Jane'}
                     ]
            }
            },
            {'300': {'ind1': ' ',
                     'ind2': ' ',
                     'subfields': [
                        {'a': '1 online resource (1 map) :'},
                        {'b': 'col.'}
                     ]
            }
            },
            {'690': {'ind1': '',
                     'ind2': '',
                     'subfields': [
                         {'a': 'Test'},
                         {'b': 'Subject'}
                     ]
            }
            },
            {'856': {'ind1': '4',
                     'ind2': '0',
                     'subfields': [
                         {'u': 'http://example.org/foo'}
                     ]
            }
            }
        ]
        test['leader'] = '00104abc 1234567Az 1234'
        test_object = IIIFDataExtractionFromMarc.from_dict(test)
        self.assertEqual(test_object.show_title(), 'A Title of a CHO')
        self.assertEqual(test_object.show_description(), '1 online resource (1 map) : col.')
        self.assertEqual(test_object.show_metadata(), [{'label': 'Local Subject', 'value': 'Test Subject'},
                                                       {'label': 'Electronic Location and Access', 'value': 'http://example.org/foo'}])


if __name__ == "__main__":
    unittest.main()
