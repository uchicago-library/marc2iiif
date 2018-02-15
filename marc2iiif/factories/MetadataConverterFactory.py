"""a factory class to build an instance of a metadata converter 
"""

from ..converters.Marc2IIIFConverter import Marc2IIIFConverter


class MetadataConverterFactory(object):
    def __init__(self, request):
        self.request = request

    def build(self):
        if self.request == 'marc2iiif':
            return Marc2IIIFConverter()
