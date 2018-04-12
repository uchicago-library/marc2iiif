
from os import scandir
from os.path import isdir, isfile
from pymarc import MARCReader

class MarcFilesFromDisk:

    __name__ = "MarcFilesFromDisk"

    def __init__(self, file_path):
        if isdir(file_path):
            records = [x for x in self._find_files_on_disk(file_path)]
        elif isfile(file_path):
            records = [x.as_dict() for x in MARCReader(open(file_path, 'rb'))]
        else:
            msg = "{} is neither a directory nor a regular file on this disk!".format(file_path)
            raise ValueError(msg)
        self.records = records

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
            title_parts = [x.get("245").get("subfields") for x in a_marc_record.get("fields") if x.get("245")][0]
            major_title = [x.get("a") for x in title_parts if x.get("a")][0]
            tail_title = [x.get("b") for x in title_parts if x.get("b")][0]
            responsibility = [x.get("c") for x in title_parts if x.get("c")]
            if major_title:
                self.label = major_title
            else:
                self.label = None
            if tail_title:
                self.full_title = major_title + tail_title
            if responsibility:
                self.responsibility_statement = responsibility
            #self.simple_title = [x for x in a_marc_record.get('245').get('subfields') if x.get()
            