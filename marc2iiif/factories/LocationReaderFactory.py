from ..readers import OnDiskReader

class LocationReaderFactory(object):
    def __init__(self, request):
        self.request = request


    def build(self):
        return NotImplemented