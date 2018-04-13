
from itertools import chain
from os import scandir
from os.path import isdir, isfile
from pymarc import MARCReader

class MarcFilesFromDisk:

    __name__ = "MarcFilesFromDisk"

    def __init__(self, file_path):

        if isdir(file_path):
            self.path = file_path
        elif isfile(file_path):
            self.file = file_path
        else:
            msg = "{} is neither a directory nor a regular file on this disk!".format(file_path)
            raise ValueError(msg)

    def __iter__(self):
        if getattr(self, 'path', None):
            generator = self._find_files_on_disk(self.path)
            return generator
        else:
            return [x.as_dict() for x in MARCReader(open(file_path, 'rb'))][0]

    def _find_files_on_disk(self, a_path):
        """a function to find marc files in a particular directory on-disk
        """
        for n_item in scandir(a_path):
            if n_item.is_file() and n_item.path.endswith(".mrc"):
                reader = MARCReader(open(n_item.path,'rb'))
                for record in reader:
                    yield record.as_dict()
            elif n_item.is_dir():
                yield from self._find_files_on_disk(n_item.path)

class IIIFDataExtractionFromMarc:

    __name__ = "IIIFDataExtractionFromMarc"

    def __init__(self, a_marc_record):
        if not isinstance(a_marc_record, dict):
            msg = "{} can only take a dict passed to init".format(self.__name__)
            raise ValueError(msg)
        else:
            self.label = a_marc_record
            self.description  = a_marc_record
            self.metadata = IIIFMetadataBoxFromMarc(a_marc_record)

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
            del self._title

    def set_description(self, value):
        if not isinstance(value, dict):
            raise ValueError("must pass a marc record as a dictionary to set description property")
        else:
            all_fields = [x for x in value.get("fields")]
            field_keys = list(chain(*[list(x.keys()) for x in all_fields]))
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
                    print(note)
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
            del self._description

    def set_description(self, value):
        if isinstance(value, IIIFMetadataBoxFromMarc):
            setattr(self, "_metadata", value)
        else:
            raise ValueError("must place an instance of IIIFMetadataBoxFromMarc into this field")

    def get_metadata(self, value):
        if hasattr(self, '_metadata'):
            return getattr(self, '_metadata')

    def del_description(self):
        if hasattr(self, '_description'):
            del self._description    
    
    label = property(get_label, set_label, del_label)
    description = property(get_description, set_description, del_description)
    metadata = property(get_metadata, set_metadata, del_metadata)

class IIIFMetadataBoxFromMarc:

    __name__ = "IIIFMetadataBoxFromMarc"

    def __init__(self, a_marc_record, fields_needed):
        self.field_names = fields_needed
        self.fields = a_marc_record
        self.total = len(self.fields)

    def __dict__(self):
        output = {"metadata":[]}
        for field in self.fields:
            output["metadata"].append({"label": field.name, "value": field.value}
        return output

    def __repr__(self):
        return self.name + " with " + str(self.total) + " metadata fields"

    def __str__(self):
        return str(dict(self))

    def get_field_names(self):
        if hasattr(self, "_field_names"):
            setattr(self, "_field_names", value)

    def set_field_names(self, value):
        if isinstance(value, list):
            for n_field_name in value:
                if not isinstance(n_field_name, str):
                    raise ValueError("There cannot be a non-string element in the field_names property")
        else:
            raise ValueError("IIIFMetadataBoxFromMarc field_names must be a list")
        setattr(self, "_field_names", value)

    def field_names(self):
        if hasattr(self, "_field_names"):
            del self._field_names

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
            del self._total

    field_names = property(get_field_names, set_field_names, del_field_names)
    fields = property(get_fields, set_fields, del_fields)
    total = property(get_total, set_total, del_total)