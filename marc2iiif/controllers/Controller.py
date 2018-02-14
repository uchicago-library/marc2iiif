from ..factories import MetadataConverterFactory, MetadataEvaluatorFactory
from ..factories import LocationReaderFactory

class Controller(object):
    def __init__(self, evaluator_type, location_type, conversion_type):
        self.metadata_evaluator = MetadataEvaluatorFactory.MetatadataEvaluatorFactory(evaluator_type).build()
        self.metadata_finder = LocationReaderFactory.LocationReaderFactory(location_type).build()
        self.metadata_converter = MetadataConverterFactory.MetadataConverterFactory(conversion_type).build()