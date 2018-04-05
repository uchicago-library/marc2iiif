
from os import scandir
from os.path import isdir, isfile
from pymarc import MARCReader

class MarcFilesFromDisk:
    def __init__(self, file_path):
        if isdir(file_path):
            self.files = self._find_files_on_disk(file_path)
        elif isfile(file_path):
            self.files = [MARCReader(file_path)]

    def _find_files_on_disk(self, a_path):
        """a function to find marc files in a particular directory on-disk
        """
        for n_item in scandir(a_path):
            if n_item.is_file():
                return MARCReader(n_item.path)
            elif n_item.is_dir():
                yield from self._find_files_on_disk(n_item.path)



