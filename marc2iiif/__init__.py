
from os import scandir
from os.path import isdir, isfile
from pymarc import MARCReader

class MarcFilesFromDisk:
    def __init__(self, file_path):
        print(file_path)
        if isdir(file_path):
            print("hi")
            records = self._find_files_on_disk(file_path)
        elif isfile(file_path):
            records = [MARCReader(file_path)]
        print([x for x in records])

    def _find_files_on_disk(self, a_path):
        """a function to find marc files in a particular directory on-disk
        """
        for n_item in scandir(a_path):
            if n_item.is_file() and n_item.path.endswith(".mrc"):
                reader = MARCReader(open(n_item.path,'rb'))
                for record in reader:
                    yield record
            elif n_item.is_dir():
                yield from self._find_files_on_disk(n_item.path)
