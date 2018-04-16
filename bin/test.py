"""a test script to show proof of concept of the application
"""

from argparse import ArgumentParser
import json
from os import _exit, scandir
from marc2iiif import MarcFilesFromDisk, IIIFDataExtractionFromMarc
from sys import stdout

__VERSION__ = "0.1.0"

def find_marc_files(path):
    """a function to find marc files in a particular directory on-disk
    """
    MarcFilesFromDisk(path)

def main():
    arguments = ArgumentParser(
        description="A cli module to prototype the marc2iiif converter; version " + __VERSION__)
    arguments.add_argument('location_of_files', type=str, action='store',
                           help="The place to find the files that need to be converted")
    parsed_args = arguments.parse_args()
    try:
        location = parsed_args.location_of_files
        marc_readers = MarcFilesFromDisk(location)
        for n in marc_readers:
            p = IIIFDataExtractionFromMarc(n)
            #print(json.dumps(p.to_dict(), indent=4))
        return 0
    except KeyboardInterrupt:
        return 131


if __name__ == "__main__":
    _exit(main())
