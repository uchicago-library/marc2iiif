"""a concrete instance of Writer class to handle writing output directo to local disk
"""
from .Writer import Writer

class OnDiskWriter(Writer):
    def __init__(self):
        pass

    
    def write(self, location_to_write_to):
        return NotImplemented