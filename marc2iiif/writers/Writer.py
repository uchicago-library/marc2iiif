

from abc import ABC, abstractclassmethod


class Writer(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def write(self, a_location):
        pass
