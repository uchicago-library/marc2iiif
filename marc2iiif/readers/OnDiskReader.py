"""an concrete instance of class Reader that can be used to read files stored on locally accessible disk
"""

from .Reader import Reader


class OnDiskReader(Reader):
    def __init__(self):
        self.items = []

    def read(self):
        return NotImplemented
