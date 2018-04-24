
from itertools import chain
from os import scandir
from os.path import dirname, isdir, isfile
from pymarc import MARCReader
from re import compile as re_compile

from .constants import DESCRIPTION_LOOKUPS, LABEL_LOOKUP, TITLE_LOOKUPS
from .utils import combine_subfields_into_one_value, default_identifier_extraction, match_single_file, search_for_marc_file

# TODO write abstract file reader class and inherit MarcFilesFromDisk from that

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

    def show_title(self):
        """a method to show the title of the IIIF record

        It retrieves the label from the metadata information that the instance delegates metadata collection to

        :rtype str
        """
        if getattr(self, 'metadata', None):
            if hasattr(self.metadata, "_label"):
                return self.metadata.label
        return 'None'

    def show_description(self):
        if getattr(self, 'metadata', None):
            if hasattr(self.metadata, "_label"):
                return self.metadata.description
        return None

    def show_metadata(self):
        if getattr(self, 'metadata', None):
            if hasattr(self.metadata, "fields"):
                return self.metadata.fields

    def add_metadata(self, a_dict):
        if isinstance(a_dict, dict):
            if not a_dict.get("field_name") or not a_dict.get("field_value"):
                raise ValueError("the input must have field_name and field_value defined")
            else:
               new = IIIFMetadataField(a_dict.get("field_name"), a_dict.get("field_value")) 
               self.metadata.add_field(new)
        else:
            raise TypeError("must be a dict")

    def change_title(self, value):
        self.metadata.label = value

    def change_description(self, value):
        self.metadata.description = value

    def remove_metadata(self, a_dict):
        if isinstance(a_dict, dict):
            field_name = list(a_dict.keys())[0]
            field_value = a_dict.get(list(a_dict.keys())[0])

    def _search_for_metadata_field(self, name, query_term):
        return self.metadata._find_field(name, query_term)

    def modify_metadata(self, field_to_change, new_value):
        if isinstance(field_to_change, dict) and isinstance(new_value, str):
            result = self._search_for_metadata_field(list(field_to_change.keys())[0],
                                                     field_to_change.get(list(field_to_change.keys())[0]))
            if result and len(result) == 1:
                self.metadata._replace_field_value(result[0], new_value)
        else:
            raise TypeError("first param is not a dict or second param is not a string")


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
        fields = a_dict.get("fields")
        match_titles = [list(set(x.keys()) & set(TITLE_LOOKUPS))[0] 
            for x in fields if list(set(x.keys() & set(TITLE_LOOKUPS)))]
        match_descriptions = [list(set(x.keys()) & set(DESCRIPTION_LOOKUPS))[0] 
            for x in fields  if list(set(x.keys() & set(DESCRIPTION_LOOKUPS)))]
        match_mdata_fields = [list(set(x.keys()) & set(LABEL_LOOKUP.keys()))[0]
            for x in fields if list(set(x.keys()) & set(LABEL_LOOKUP.keys()))]
        label = "An untitled Cultural Heritage Object"
        description = "This Cultural Heritage Object does not have a description"
        metadata = []
        for key in match_titles + match_descriptions + match_mdata_fields:
            if key in TITLE_LOOKUPS:
                subfields = [x.get(key).get("subfields") for x in fields if x.get(key)][0]
                label = [x for x in subfields if 'a' in x.keys()][0].get("a")
            elif key in DESCRIPTION_LOOKUPS:
                description = [combine_subfields_into_one_value(x.get(key).get("subfields")) for x in fields if x.get(key)][0]
            elif key in LABEL_LOOKUP.keys():
                metadata.append(
                    IIIFMetadataField(LABEL_LOOKUP.get(key),
                    [combine_subfields_into_one_value(x.get(key).get("subfields"))
                        for x in fields if x.get(key)][0])
                )
        if metadata:
            pot_id = [x.value for x in metadata if x.label == 'Electronic Location and Access']
            if pot_id:
                identifier = pot_id[0]
        return cls(label, description, identifier, metadata)

    def add_field(self, a_field):
        if isinstance(a_field, IIIFMetadataField):
            if hasattr(self, '_fields'):
                self._fields.append(a_field)
            else:
                self.fields = [a_field]
        else:
            raise ValueError("fields can only contain IIIFMetadataFields")

    def _find_field(self, field_name, field_value):
        for n in self._fields:
            if n.label == field_name and n.value == field_value:
                return [n]
        return []

    def _replace_field_value(self, field_to_mod, new_value):
        self._fields[self._fields.index(field_to_mod)].value = new_value

    def get_fields(self):
        output = []
        if hasattr(self, "_fields"):
            for n_field in getattr(self, "_fields"):
                output.append({"label": n_field.label, "value": n_field.value})
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
