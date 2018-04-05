"""a test script to show proof of concept of the application
"""

from argparse import ArgumentParser
from os import _exit, scandir
from pymarc import MARCReader
from sys import stdout

__VERSION__ = "0.1.0"

def find_marc_files(path):
    """a function to find marc files in a particular directory on-disk
    """
    for n_item in scandir(path):
        if n_item.is_file():
            return n_item.path
        elif n_item.is_dir():
            yield from find_marc_files(n_item.path)


def main():
    arguments = ArgumentParser(
        description="A cli module to prototype the marc2iiif converter; version " + __VERSION__)
    arguments.add_argument('location_of_files', type=str, action='store',
                           help="The place to find the files that need to be converted")
    parsed_args = arguments.parse_args()
    try:
        location = parsed_args.location_of_files
        find_marc_files(location) 
        return 0
    except KeyboardInterrupt:
        return 131


if __name__ == "__main__":
    _exit(main())
