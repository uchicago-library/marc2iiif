"""a factory class to build an instance of a location reader
"""
from ..readers import OnDiskReader


class LocationReaderFactory(object):
    def __init__(self, request):
        self.request = request

    def build(self):
        if self.request == 'ondisk':
            return OnDiskReader.OnDiskReader()
