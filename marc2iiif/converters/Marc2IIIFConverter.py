"""a class to take some marc data and convert it to a metadata block that can be inserted into a IIIF record
"""

from .Converter import Converter

class Marc2IIIFConverter(Converter):
    def __init__(self):
        pass

    def convert(self):
        return NotImplemented