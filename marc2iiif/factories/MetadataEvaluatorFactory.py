from ..evaluators import MarcEvaluator

class MetatadataEvaluatorFactory(object):
    def __init__(self, request):
        self.request = request


    def build(self):
        return NotImplemented