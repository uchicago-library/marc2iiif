
from io import BytesIO
import unittest

from marc2iiif import IIIFDataExtractionFromMarc, IIIFMetadataBoxFromMarc, IIIFMetadataField


class Tests(unittest.TestCase):
    def setUp(self):
        # need to setup a sample MARC record in a dictionary
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
        self.data = test

    def testModifyingMetadata(self):
        """a test to modify a partricular metadata field with a new value
        """
        test_object = IIIFDataExtractionFromMarc.from_dict(self.data)
        test_object.modify_metadata(
            {'Local Subject': "Test Subject"}, 'A new subject')
        check = False
        for n in test_object.show_metadata():
            if n.get('value') == 'A new subject':
                check = True
                break
        self.assertEqual(check, True)

    def testRemoveMetadata(self):
        """a test to remove a particular metadata field
        """
        test_object = IIIFDataExtractionFromMarc.from_dict(self.data)
        test_object.remove_metadata({"Local Subject": "Test Subject"})
        check = False
        for n in test_object.show_metadata():
            if n.get('value') == 'Local Subject':
                check = True
                break
        self.assertEqual(check, False)

    def testChangeTitle(self):
        """a test to change the title of the IIIF record from original title to new title
        """
        test_object = IIIFDataExtractionFromMarc.from_dict(self.data)
        test_object.change_title('A brand new title')
        self.assertEqual(test_object.show_title(), 'A brand new title')

    def testChangeDescription(self):
        """a test to successfully change the description for the record from a pre-defined description
        """
        test_object = IIIFDataExtractionFromMarc.from_dict(self.data)
        test_object.change_description(
            'A totally new description that is way better than the old description')
        self.assertEqual(test_object.show_description(
        ), 'A totally new description that is way better than the old description')

    def testBuildIIIFDataExtractionFromMarc(self):
        """a test to successfully build a new instance of IIIFDataExtractionFromMarc
        """
        metadata_box = IIIFMetadataBoxFromMarc('a label',
                                               'a description',
                                               '/foo/bar', [
                                                   IIIFMetadataField(
                                                       "a field", "a value")
                                               ])
        new_object = IIIFDataExtractionFromMarc(metadata_box)
        self.assertEqual(new_object.show_title(), 'a label')
        self.assertEqual(new_object.show_description(), 'a description')

    def testBuildIIIFMetadataBoxFromMarc(self):
        """a test to successfully create a new IIIFMetadataBoxFromMarc instance
        """
        new_object = IIIFMetadataBoxFromMarc('a label',
                                             'a description',
                                             '/foo/bar', [
                                                 IIIFMetadataField(
                                                     "a field", "a value")
                                             ])
        self.assertEqual(new_object.label, 'a label')
        self.assertEqual(new_object.description, 'a description')
        self.assertEqual(new_object.identifier, '/foo/bar')

    def testBuildIIIFMetadataField(self):
        """a test to  successfully create a new IIIFMetadataField instance
        """
        new_object = IIIFMetadataField("a field", "a value")
        self.assertEqual(new_object.label, 'a field')
        self.assertEqual(new_object.value, 'a value')

    def testLoadFromDict(self):
        """a test to successfully load an instance of IIIDataExtractionFromMarc from a dictionary containing a MARC record
        """
        test_object = IIIFDataExtractionFromMarc.from_dict(self.data)
        self.assertEqual(test_object.show_title(), 'A Title of a CHO')
        self.assertEqual(test_object.show_description(),
                         '1 online resource (1 map) : col.')
        self.assertEqual(test_object.show_metadata(), [{'label': 'Local Subject', 'value': 'Test Subject'},
                                                       {'label': 'Electronic Location and Access', 'value': 'http://example.org/foo'}])


if __name__ == "__main__":
    unittest.main()
