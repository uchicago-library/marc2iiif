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

    def evaluate(self, location_of_metadata):
        # first populate a list of items using the selected metadata finder
        items = self.metadata_finder.read(location_of_metadata)
        output = []
        for n_item in items:
            # TODO: need a IIIFManifest builder class
            #new_manifest = IIIFManifest()
            # next need to extract the desired metadata from a specific metadata file
            evaluated_data = self.metadata_evaluator.evaluate(n_item)
            # third: need to convert the desired extracted metadata into a IIIF block of meatadata
            converted_data = self.metadata_converter.convert(evaluated_data)
            # TODO: IIIFManifest class needs to method add_metadata that will add a block and auto-generate label and description
            # new_manifest.add_metadata(converted_data)
            # new_manifest.add_metadata(converted_data)
            output.append(converted_data)
        return output
