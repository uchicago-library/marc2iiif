
from .Reader import Reader

class OnDiskReader(Reader):
    def _init__(self, location):
        self.location = location
        self.items = []
    
    def read(self):
        return NotImplemented