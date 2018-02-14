"""an abstract class Reader that requires all concret instances have a method read
"""

from abc import ABC, abstractclassmethod


class Reader(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def read(self):
        pass
