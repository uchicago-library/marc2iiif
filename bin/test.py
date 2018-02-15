"""a test script to show proof of concept of the application
"""

from argparse import ArgumentParser
from os import _exit
from sys import stdout

from marc2iiif.controllers.Controller import Controller

__VERSION__ = "0.1.0"


def main():
    arguments = ArgumentParser(
        description="A cli module to prototype the marc2iiif converter; version " + __VERSION__)
    arguments.add_argument('location_of_files', type=str, action='store',
                           help="The place to find the files that need to be converted")
    parsed_args = arguments.parse_args()
    try:
        location = parsed_args.location_of_files
        c = Controller('marc', 'ondisk', 'marc2iiif')
        metadata_packages = c.evaluate(location)
        # TODO: need to write a IIIFWriterFactory class that will return an instance of a IIIFWriter for variety of write purposes
        writer = IIIFWriterFactory("ondisk").build()
        for n_package in metadata_packages:
            # need to write the IIIF Manifests somewhere
            writer.write(n_package) 
            n_package.write()
        stdout.write("hello from the test cli\n")
        return 0
    except KeyboardInterrupt:
        return 131


if __name__ == "__main__":
    _exit(main())
