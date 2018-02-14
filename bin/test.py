
from argparse import ArgumentParser
from os import _exit
from sys import stdout

from marc2iiif.controllers.Controller import Controller

__VERSION__ = "0.1.0"

def main():
    arguments = ArgumentParser(description="A cli module to prototype the marc2iiif converter; version " + __VERSION__)
    arguments.add_argument('location_of_files', type=str, action='store', help="The place to find the files that need to be converted")
    parsed_args = arguments.parse_args()
    try:
        location = parsed_args.location_of_files
        c = Controller('marc', location, 'marc2iiif')
        stdout.write("hello from the test cli\n")
        return 0
    except KeyboardInterrupt:
        return 131
    
if __name__ == "__main__":
    _exit(main())