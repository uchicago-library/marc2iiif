"""a class to take some MARC binary file and extract the useful metadata from it 
"""
from .Evaluator import Evaluator

class MarcEvaluator(Evaluator):
    def __init__(self):
        pass

    def evaluate(self, thing_to_evaluate):
        return NotImplemented