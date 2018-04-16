
from itertools import chain
from os import scandir
from os.path import dirname, isdir, isfile
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
            self.records = self._build_generator_of_files(file_path, self.search_for_marc_file)
        elif isfile(file_path):
            self.records = self._build_generator_of_files(file_path, self.match_single_file)
        else:
            msg = "{} is neither a directory nor a regular file on this disk!".format(file_path)
            raise ValueError(msg)

    def __iter__(self):
        return self.records

    def match_single_file(self, src, pot_match=None):
        if pot_match:
            if src == pot_match:
                return True
        return False

    def search_for_marc_file(self, src, pot_match=None):
        if src.endswith('mrc'):
            return True
        else:
            return False

    def _build_generator_of_files(self, a_path, callback=None):
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
        out["@id"] = "https://iiif-manifest.lib.uchicago.edu/"
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

    def __init__(self, fields):
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
        def default_identifier_extraction(self, value):
            return value.split("https://pi.lib.uchicago.edu/1001/")[1]

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
                    print(default_identifier_extraction(full_value))
 
        return cls(fields)


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
