"""a test script to show proof of concept of the application
"""

from argparse import ArgumentParser
import json
from os.path import abspath, dirname, normpath, join, exists
from os import _exit, getcwd, scandir, mkdir, sep
from marc2iiif import IIIFDataExtractionFromMarc
from re import compile as re_compile
from sys import stdout

__VERSION__ = "0.1.0"

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
            p = IIIFDataExtractionFromMarc.from_dict(n)
            data = p.to_dict()
            json_id = data["@id"].split("https://iiif-manifest.lib.uchicago.edu/")[1] + ".json"
            json_id = normpath(abspath(join(getcwd(), "manifests", json_id)))
            directories = dirname(json_id).split(sep)
            if re_compile("^([A-Z][:])").match(json_id):
                drive_name = re_compile("^([A-Z][:])").match(json_id).group(1)
                directory_path = '/'.join(directories[1:])
                new = drive_name + sep
                for f in directory_path.split("/"):
                    new = join(new, f)
                    if not exists(new):
                        mkdir(new)
                with open(json_id, "w+", encoding="utf-8") as wf:
                    json.dump(data, wf, indent=4)
        return 0
    except KeyboardInterrupt:
        return 131


if __name__ == "__main__":
    _exit(main())