
from ..writers import OnDiskWriter

class IIIFWriterFactory(object):
    def __init__(self, order):
        self.request = order


    def build(self):
        if self.request == 'ondisk':
            return OnDiskWriter.OnDiskWriter()
