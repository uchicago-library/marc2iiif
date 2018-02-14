
from abc import ABC, abstractclassmethod

class Evaluator(ABC):
    def __init__(self, input_file, input_type):
        self.input_file = input_file
        self.input_type = input_type

    @abstractclassmethod
    def evaluate(self):
        pass