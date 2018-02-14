"""an abstract class for Evaluator. It requires that any concret instance have a method evaluate
"""

from abc import ABC, abstractclassmethod

class Evaluator(ABC):
    @abstractclassmethod
    def evaluate(self, something_to_evaluate):
        pass