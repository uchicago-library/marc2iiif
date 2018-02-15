"""a factory class to instantiate a metadata evaluator instance
"""

from ..evaluators.MarcEvaluator import MarcEvaluator


class MetatadataEvaluatorFactory(object):
    def __init__(self, request):
        self.request = request

    def build(self):
        if self.request == 'marc':
            return MarcEvaluator()
