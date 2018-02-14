"""an concrete instance of class Reader that can be used to read files stored on locally accessible disk
"""

from abc import ABC, abstractclassmethod

class Reader(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def read(self):
        pass