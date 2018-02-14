
from abc import ABC, abstractclassmethod

class Reader(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def read(self):
        pass