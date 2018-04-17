
from itertools import chain
from os import scandir
from os.path import dirname, isdir, isfile
from pymarc import MARCReader
from re import compile as re_compile

from .constants import LABEL_LOOKUP
from .utils import default_identifier_extraction, match_single_file, search_for_marc_file

# TODO write abstract file reader class and inherit MarcFilesFromDisk from that

class MarcFilesFromDisk:
    """a class to be used for reading MARC records from disk
    """
    __name__ = "MarcFilesFromDisk"

    def __init__(self, file_path):
        """instantiates an instance of MarcFilesFromDisk

        :param str file_path: an absolute file path accessible on the machine running the program

        :rtype :instance:`MarcFilesFromdisk`
        """
        # check if the path is a directory in which case there are likely to be more than 
        # one more records to evaluate
        if isdir(file_path):
            self.records = self._build_generator_of_files(file_path, search_for_marc_file)
        # check of the path is a file in which case there is only one marc record in this batch
        elif isfile(file_path):
            self.records = self._build_generator_of_files(file_path, match_single_file)
        else:
            msg = "{} is neither a directory nor a regular file on this disk!".format(file_path)
            raise ValueError(msg)

    def __iter__(self):
        """a method to iterate through the records in the instance

        :rtype lis
        """
        return self.records

    def _build_generator_of_files(self, a_path, callback=None):
        """a private method to build a generator out of the files in the inputted file_path

        It will return a generator of MARC records as dictionaries that look like
        {"fields":}
        :param str a_path: a particular path on-disk
        :param str callback: a function to use for checking if the path is a file and
        satisfies the requirement
        """
        if isfile(a_path):
            path = dirname(a_path)
        else:
            path = a_path
        for n_item in scandir(path):
            if n_item.is_dir():
                yield from self._build_generator_of_files(n_item.path, callback=callback)
            elif n_item.is_file() and callback(n_item.path, pot_match=a_path):
                reader = MARCReader(open(n_item.path, 'rb'))
                for record in reader:
                    yield record.as_dict()

class IIIFDataExtractionFromMarc:
    """a class to be used for extracting IIIF relevant data from a MARC record 
    """
    __name__ = "IIIFDataExtractionFromMarc"

    def __init__(self, a_marc_record):
        if not isinstance(a_marc_record, dict):
            msg = "{} can only take a dict passed to init".format(self.__name__)
            raise ValueError(msg)
        else:
            self.label = a_marc_record
            self.description  = a_marc_record
            self.metadata = IIIFMetadataBoxFromMarc.from_dict(a_marc_record)
            
    def __repr__(self):
        return self.__name__ + " for " + self.label

    def __str__(self):
        return "label: " + self.label + ", description: " + self.description

    def to_dict(self):
        out = {}
        out["@context"] = "https://iiif.io/api/presentations/2/context.json"
        out["@id"] = "https://iiif-manifest.lib.uchicago.edu/" + self.metadata.identifier
        out["metadata"] = self.metadata.to_dict()
        out["description"] = self.description
        out["label"] = self.label
        return out

    def set_label(self, value):
        if not isinstance(value, dict):
            raise ValueError("must pass a marc record as a dictionary to set label property")
        else:
            title_subfields =  list(chain(*[x.get("subfields") for x in [x.get("245") for x in value.get("fields") if x.get("245")]]))
            main_title_search = [x for x in title_subfields if x.get("a")]
            if main_title_search:
                setattr(self, '_title', main_title_search[0].get("a"))
            else:
                raise ValueError("title could not be found in this marc record")

    def get_label(self):
        if hasattr(self, '_title'):
            return getattr(self, '_title')

    def del_label(self):
        if hasattr(self, '_title'):
            delattr(self, "_title")

    def set_description(self, value):
        if not isinstance(value, dict):
            raise ValueError("must pass a marc record as a dictionary to set description property")
        else:
            all_fields = [x for x in value.get("fields")]
            note = ""
            description = ""
            for thing in all_fields:
                keys = list(thing.keys())
                description_match = [x for x in keys if x.startswith('3')]
                note_match = [x for x in keys if x.startswith('5')]
                if note_match:
                    subfields = thing.get(list(thing.keys())[0]).get("subfields")
                    for subfield in subfields:
                        val = [v for x,v in subfield.items()][0]
                        note += " " + val
                if description_match:
                    subfields = thing.get(list(thing.keys())[0]).get("subfields")
                    for subfield in subfields:
                        val = [v for x,v in subfield.items()][0]
                        description += " " + val
            output = ""
            if note != "":
                output += note
            if description != "":
                output += " " + description
            output = output.strip()
            setattr(self, "_description", output)

    def get_description(self):
        if hasattr(self, '_description'):
            return getattr(self, '_description')
    
    def del_description(self):
        if hasattr(self, '_description'):
            delattr(self, "_descripton")

    def set_metadata(self, value):
        if isinstance(value, IIIFMetadataBoxFromMarc):
            setattr(self, "_metadata", value)
        else:
            raise ValueError("must place an instance of IIIFMetadataBoxFromMarc into this field")

    def get_metadata(self):
        if hasattr(self, '_metadata'):
            return getattr(self, '_metadata')
   
    def del_metadata(self):
        if hasattr(self, '_metadata'):
            delattr(self, "_metadata")

    label = property(get_label, set_label, del_label)
    description = property(get_description, set_description, del_description)
    metadata = property(get_metadata, set_metadata, del_metadata)

class IIIFMetadataBoxFromMarc:

    __name__ = "IIIFMetadataBoxFromMarc"

    def __init__(self, identifier, fields):
        self.identifier = identifier
        self.fields = fields

    def __repr__(self):
        return self.__name__ + " with " + str(self.total) + " metadata fields"

    def __str__(self):
        output = "metadata:"
        output += "\n"
        for n_field in self.fields:
            output += "\t" + str(n_field) + "\n"
        return output

    def to_dict(self):
        out = []
        for a_field in self.fields:
            out.append(a_field)
        return out

    def get_fields(self):
        output = []
        if hasattr(self, "_fields"):
            for n_field in getattr(self, "_fields"):
                output.append({"field": n_field.field, "label": n_field.value})
        return output

    def set_fields(self, value):
        for a_field in value:
            if not isinstance(a_field, IIIFMetadataField):
                raise ValueError("fields can only contain IIIFMetadataField instances")
        self._fields = value

    @classmethod
    def from_dict(cls, a_dict):
        fields = []
        for thing in [x for x in a_dict.get("fields")]:
            keys = [key for key in thing.keys() if not key.startswith('00')]
            m = [(LABEL_LOOKUP.get(x), thing.get(x).get("subfields")) for x in keys]
            if m:
                full_value = ""
                for n in m[0][1]:
                    full_value += " " + (n.get(list(n.keys())[0]))
                    if m[0][0]:
                        field = IIIFMetadataField(m[0][0], full_value)
                        fields.append(field)
                if m[0][0] and 'Electronic Location and Access' in m[0][0]:

                    pot_identifier = default_identifier_extraction(full_value)
                    if pot_identifier[0]:
                        identifier = pot_identifier[1]
                    else:
                        identifer = ""

        return cls(identifier, fields)


    def add_field(self, a_field):

        if isinstance(a_field, IIIFMetadataField):
            if hasattr(self, '_fields'):
                self._fields.append(a_field)
            else:
                self.fields = [a_field]
        else:
            raise ValueError("fields can only contain IIIFMetadataFields")

    def del_fields(self):
        if hasattr(self, "_fields"):
            del self._fields 

    def set_total(self, value):
        if isinstance(value, int):
            setattr(self, "_total", value)
        else:
            raise ValueError("total property can only be an integer")
    
    def get_total(self, value):
        if hasattr(self, "_total"):
            return hasattr(self, "_total")

    def del_total(self):
        if hasattr(self, "_total"):
            delattr(self, "_total")

    def set_identifier(self, value):
            setattr(self, '_identifier', value)

    def get_identifier(self):
        if hasattr(self, '_identifier'):
            return getattr(self, '_identifier')
   
    def del_identifier(self):
        if hasattr(self, '_identifier'):
            delattr(self, '_identifier')

    identifier = property(get_identifier, set_identifier, del_identifier)
    fields = property(get_fields, set_fields, del_fields)
    total = property(get_total, set_total, del_total)


class IIIFMetadataField:

    __name__ = "IIIFMetadataField"

    def __init__(self, name, value):
        self.field = name
        self.value = value

    def __repr__(self):
        return "{}:{}".format(self.field, self.value)

    def __str__(self):
        return "{}: {}".format(self.field, self.value)

    def __dict__(self):
        return {"label": self.field, "value": self.value}

    def get_field(self):
        return getattr(self, "_field")

    def set_field(self, value):
        if isinstance(value, str):
            setattr(self, "_field", value)
        else:
            raise ValueError("field must be a string")

    def del_field(self):
        if hasattr(self, "_field"):
            delattr(self, "_field")
            delattr(self, "_field")

    def get_value(self):
        return getattr(self, "_value")

    def set_value(self, value):
        if isinstance(value, str):
            setattr(self, "_value", value)
        else:
            raise ValueError("value must be a string")

    def del_value(self):
        if hasattr(self, "_value"):
            delattr(self, "_value")

    @classmethod
    def load_from_dict(cls, a_subfield):
        pass

    field = property(get_field, set_field, del_field)
    value = property(get_value, set_value, del_value)
