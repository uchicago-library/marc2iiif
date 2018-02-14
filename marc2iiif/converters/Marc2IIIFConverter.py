
from .Converter import Converter

class Marc2IIIFConverter(Converter):
    def __init__(self, input):
        self.input = input
    
    def convert(self):
        return NotImplemented