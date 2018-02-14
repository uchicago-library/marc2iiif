from ..converters import Marc2IIIFConverter

class MetadataConverterFactory(object):
    def __init__(self, request):
        self.request = request


    def build(self):
        return NotImplemented