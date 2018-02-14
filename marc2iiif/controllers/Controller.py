"""the main actor in the application that coordinates all the different actor classes and their output
"""

from ..factories import MetadataConverterFactory, MetadataEvaluatorFactory
from ..factories import LocationReaderFactory


class Controller(object):
    def __init__(self, evaluator_type, location_type, conversion_type):
        self.metadata_evaluator = MetadataEvaluatorFactory.MetatadataEvaluatorFactory(
            evaluator_type).build()
        self.metadata_finder = LocationReaderFactory.LocationReaderFactory(
            location_type).build()
        self.metadata_converter = MetadataConverterFactory.MetadataConverterFactory(
            conversion_type).build()

    def find_files(self, location):
        self.metadata_finder

    def evaluate_(self):
        for n_item in self.metadata_finder.items:
            return self.metadata_evaluator.evaluate(n_item)
