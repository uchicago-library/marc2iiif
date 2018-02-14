"""an abstract class Converter that requires all concrete instances have a method convert and a property input
"""

from abc import ABC, abstractmethod


class Converter(ABC):
    def __init__self(self, input):
        self.input = input

    @abstractmethod
    def convert(self):
        pass
