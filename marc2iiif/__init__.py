
from itertools import chain
from os import scandir
from os.path import isdir, isfile
from pymarc import MARCReader
from re import compile as re_compile

LABEL_LOOKUP = {
    "250": "Edition Statement",
    "254": "Musical Presentation Statement",
    "255": "Cartographic Mathemtical Data",
    "256": "Computer File Characteristic",
    "257": "Country of Producing Entity",
    "258": "Philatelic Issue Data",
    "260": "Publication, Distribution, etc (Imprint)",
    "263": "Projected Publication Date",
    "264": "Production, Publication, Publication, Distribution, Manufacture, and Copyright Notice",
    "270": "Address",
    "600": "Subject Added Entry - Personal Name",
    "610": "Subject Added Entry - Corporate Name",
    "611": "Subject Added Entry - Meeting Name",
    "630": "Subject Added Entry - Uniform Title",
    "647": "Subject Added Entry - Named Event",
    "648": "Subject Added Entry - Chronological Term",
    "650": "Subject Added Entry = Topical Term",
    "651": "Subject Added Entry - Geographic Name",
    "653": "Index Term - Uncontrolled",
    "654": "Subject Added Entry - Faceted Topical Term",
    "655": "Index Term - Genre/Form",
    "656": "Index Term - Occupation",
    "657": "Index Term - Function",
    "658": "Index Term - Curriculum Objective",
    "662": "Subject Added Entry - Hierarchical Place Name",
    "690": "Local Subject",
    "691": "Local Subject",
    "692": "Local Subject",
    "693": "Local Subject",
    "694": "Local Subject",
    "695": "Local Subject",
    "696": "Local Subject",
    "697": "Local Subject",
    "698": "Local Subject",
    "699": "Local Subject",
    "700": "Added Entry - Personal Name",
    "710": "Added Entry - Corporate Name",
    "711": "Added Entry - Meeting Name",
    "720": "Added Entry - Uncontrolled Name",
    "730": "Added Entry - Uniform Title",
    "740": "Added Entry - Uncontrolled Related/Analytical Title",
    "751": "Added Entry - Geographic Name",
    "752": "Added Entry - Hierarchical Place Name",
    "753": "System Details Access to Computer File",
    "754": "Added Entry - Taxonomic Identification",
    "758": "Resource Identifier",
    "760": "Main Entry Series Entry",
    "762": "Subseries Entry",
    "765": "Original Language Entry",
    "767": "Translation Entry",
    "770": "Supplement/Special Issue Entry",
    "772": "Supplement Parent Entry",
    "773": "Host Item Entry",
    "774": "Constituent Unit Entry",
    "775": "Other Edition Entry",
    "776": "Additional Physical Form Entry",
    "777": "Issued With Entry",
    "780": "Preceding Entry",
    "785": "Succeeding Entry",
    "786": "Date Source Entry",
    "787": "Other Relationship Entry",
    "800": "Series Added Entry - Personal Name",
    "810": "Series Added Entry - Corporate Name",
    "811": "Series Added Entry - Meeting Name",
    "830": "Series Added Entry - Uniform Title",
    "841": "Holdings Coded Data Values",
    "842": "Textual Physical form Designator",
    "843": "Reproduction Note",
    "844": "Name of Unit",
    "845": "Terms Governing Use and Reproduction",
    "850": "Holding Institution",
    "852": "Location",
    "853": "Captions and Pattern - Basic Bibliographic Unit",
    "854": "Captions and Pattern - Supplementary Material",
    "855": "Captions and Pattern - Indexes",
    "856": "Electronic Location and Access",
    "863": "Enumeration and Chronology- Basic Bibligraphic Unit",
    "864": "Enumeration and Chronology - Supplementary MAterial",
    "865": "Enumeration and Chronology - Indexes",
    "866": "Textual Holdings - Basic Bibliographic Unit",
    "867": "Textual Holdings - Supplementary Material",
    "868": "Textual Holdings - Indexes",
}



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
            self.metadata = IIIFMetadataBoxFromMarc.from_dict(a_marc_record)

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
            del self._description

    def set_metadata(self, value):
        if isinstance(value, IIIFMetadataBoxFromMarc):
            setattr(self, "_metadata", value)
        else:
            raise ValueError("must place an instance of IIIFMetadataBoxFromMarc into this field")

    def get_metadata(self):
        if hasattr(self, '_metadata'):
            return getattr(self, '_metadata')
   
    def del_metadata(self):
        if hasattr(self, '_description'):
            del self._description    
    
    label = property(get_label, set_label, del_label)
    description = property(get_description, set_description, del_description)
    metadata = property(get_metadata, set_metadata, del_metadata)

class IIIFMetadataBoxFromMarc:

    __name__ = "IIIFMetadataBoxFromMarc"

    def __init__(self, a_marc_record):
        self.source = a_marc_record

    def __dict__(self):
        output = {"metadata":[]}
        for field in self.fields:
            output["metadata"].append(dict(field))
        return output

    def __repr__(self):
        return self.__name__ + " with " + str(self.total) + " metadata fields"

    def __str__(self):
        output = "metadata:"
        output += "\n"
        for n_field in self.fields:
            output += "\t" + str(n_field) + "\n"
        return output

    def get_fields(self):
        output = []
        if hasattr(self, "_fields"):
            for n_field in getattr(self, "_fields"):
                output.append("{}: {}".format(n_field.field, n_field.value))
        return output

    def set_fields(self, value):
        for a_field in value:
            if not isinstance(a_field, IIIFMetadataField):
                raise ValueError("fields can only contain IIIFMetadataField instances")
        self._fields = value

    @classmethod
    def from_dict(cls, a_dict):
        def retrieve_entries(list_of_fields):
            output = []
            if list_of_fields:
                for n_item in list_of_fields:
                    label = LABEL_LOOKUP.get(n_item[0])
                    subfields = n_item[1].get("subfields")
                    if int(n_item[0]) < 800:
                        values = [x for x in subfields if not re_compile("[0-9]").search(str(x))]
                    else:
                        values = [x for x in subfields if re_compile("[0-9]").search(str(x))]
                    full_value = ""
                    for a_dict in values:
                        full_value += " " + a_dict.get(list(a_dict.keys())[0])
                    output.append((label, full_value.strip()))
            return output

        all_fields = [x for x in a_dict.get("fields")]
        output = []
        new = cls(a_dict)
        for thing in all_fields:
            keys = list(thing.keys())
            output += retrieve_entries([(x, thing.get(x)) for x in keys if re_compile("2[5-8][0-9]").search(x)])
            output += retrieve_entries([(x, thing.get(x)) for x in keys if x.startswith('6')])
            output += retrieve_entries([(x, thing.get(x)) for x in keys if re_compile("7[0-5][0-9]").search(x)])
            output += retrieve_entries([(x, thing.get(x)) for x in keys if re_compile("7[6-8][0-9]").search(x)])
            output += retrieve_entries([(x, thing.get(x)) for x in keys if re_compile("8[0-3][0-9]").search(x)])
            output += retrieve_entries([(x, thing.get(x)) for x in keys if re_compile("8[4-8][0-9]").search(x)])
        for label, value in output:
            field = IIIFMetadataField(label, value)
            new.add_field(field)
        return new        

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
            del self._total

    fields = property(get_fields, set_fields, del_fields)
    total = property(get_total, set_total, del_total)


class IIIFMetadataField:

    __name__ = "IIIFMetadataField"

    def __init__(self, name, value):
        self.field = name
        self.value = value

    def __repr__(self):
        return "{} {}:{}".format(self.__name__. self.field, self.value)

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
            del self._field

    def get_value(self):
        return getattr(self, "_value")

    def set_value(self, value):
        if isinstance(value, str):
            setattr(self, "_value", value)
        else:
            raise ValueError("value must be a string")

    def del_value(self):
        if hasattr(self, "_value"):
            del self._field

    @classmethod
    def load_from_dict(cls, a_subfield):
        pass

    field = property(get_field, set_field, del_field)
    value = property(get_value, set_value, del_value)
