
from itertools import chain
from os import scandir
from os.path import dirname, isdir, isfile
from pymarc import MARCReader
from re import compile as re_compile

from .constants import DESCRIPTION_LOOKUPS, LABEL_LOOKUP, TITLE_LOOKUPS
from .utils import combine_subfields_into_one_value, default_identifier_extraction, match_single_file, search_for_marc_file

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

    def __init__(self, metadata):
        """initializes an instance of the class

            :param str label: the 
        """
        self.metadata = metadata
            
    def __repr__(self):
        return self.__name__

    def __str__(self):
        return self.__name__

    def to_dict(self):
        out = {}
        out["@context"] = "https://iiif.io/api/presentations/2/context.json"
        out["@id"] = "https://iiif-manifest.lib.uchicago.edu/" + self.metadata.identifier
        out["metadata"] = self.metadata.to_dict()
        out["description"] = self.metadata.description
        out["label"] = self.metadata.label
        return out

    @classmethod
    def from_dict(cls, dictified_marc_record):
        if not isinstance(dictified_marc_record, dict):
            raise ValueError("can only instantiate class from a dict")

        new_metadata = IIIFMetadataBoxFromMarc.from_dict(dictified_marc_record)
        return cls(new_metadata)

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

    metadata = property(get_metadata, set_metadata, del_metadata)

class IIIFMetadataBoxFromMarc:

    __name__ = "IIIFMetadataBoxFromMarc"

    def __init__(self, label, description, identifier, fields):
        self.label = label
        self.description = description
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

    @classmethod
    def from_dict(cls, a_dict):
        fields = []
        identifier = ""
        label = ""
        description = ""
        for thing in [x for x in a_dict.get("fields")]:
            keys = [key for key in thing.keys() if not key.startswith('00')]
            description_lookups = [thing.get(x).get("subfields") for x in keys if x in DESCRIPTION_LOOKUPS]
            title_ops = [thing.get(x).get("subfields") for x in keys if x in TITLE_LOOKUPS]
            m = [(LABEL_LOOKUP.get(x), thing.get(x).get("subfields")) for x in keys if x in LABEL_LOOKUP.keys()]
            if title_ops:
                label = (title_ops[0][0]).get("a")
                if label.endswith(":") or label.endswith("/") or label.endswith(" ") or label.endswith("=") or label.endswith("."):
                    label = label[:-1]
                    label[:-1]
                    label.strip()
                else:
                    label = "An untitled Cultural Heritage Object"
            if description_lookups:
                description = combine_subfields_into_one_value(description_lookups[0])
            else:
                description = "This Cultural Heritage Object does not have a description"
            if m:
                field_name = m[0][0]
                subfield_list = m[0][1]
                field_value = combine_subfields_into_one_value(subfield_list)
                field = IIIFMetadataField(field_name, field_value)
                fields.append(field)
                if field_name == 'Electronic Location and Access':
                    pot_identifier = default_identifier_extraction(field_value)
                    if pot_identifier[0]:
                        identifier = pot_identifier[1]
                else:
                    identifier = ""

        return cls(label, description, identifier, fields)

    def add_field(self, a_field):
        if isinstance(a_field, IIIFMetadataField):
            if hasattr(self, '_fields'):
                self._fields.append(a_field)
            else:
                self.fields = [a_field]
        else:
            raise ValueError("fields can only contain IIIFMetadataFields")

    def get_fields(self):
        output = []
        if hasattr(self, "_fields"):
            for n_field in getattr(self, "_fields"):
                output.append({"field": n_field.label, "label": n_field.value})
        return output

    def set_fields(self, value):
        for a_field in value:
            if not isinstance(a_field, IIIFMetadataField):
                raise ValueError("fields can only contain IIIFMetadataField instances")
        self._fields = value

    def del_fields(self):
        if hasattr(self, "_fields"):
            delattr(self, "_fields")

    def get_label(self):
        if hasattr(self, "_label"):
            return getattr(self, "_label")

    def set_label(self, value):
        if isinstance(value, str):
            setattr(self, "_label", value)
        else:
            raise ValueError("total property can only be an integer")

    def del_label(self):
        if hasattr(self, "_label"):
            del self._fields 

    def get_description(self):
        if hasattr(self, "_description"):
            return getattr(self, "_description")

    def set_description(self, value):
        if isinstance(value, str):
            setattr(self, "_description", value)

    def del_description(self):
        if hasattr(self, "_description"):
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
    label = property(get_label, set_label, del_label)
    description = property(get_description, set_description, del_description)
    fields = property(get_fields, set_fields, del_fields)
    total = property(get_total, set_total, del_total)

class IIIFMetadataField:

    __name__ = "IIIFMetadataField"

    def __init__(self, name, value):
        self.label = name
        self.value = value

    def __repr__(self):
        return "{}:{}".format(self.label, self.value)

    def __str__(self):
        return "{}: {}".format(self.label, self.value)

    def __dict__(self):
        return {"label": self.label, "value": self.value}

    def get_label(self):
        return getattr(self, "_label")

    def set_label(self, value):
        if isinstance(value, str):
            setattr(self, "_label", value)
        else:
            raise ValueError("field must be a string")

    def del_label(self):
        if hasattr(self, "_label"):
            delattr(self, "_label")

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

    label = property(get_label, set_label, del_label)
    value = property(get_value, set_value, del_value)
