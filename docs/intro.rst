# marc2iiif

## Introduction

This is an application that will allow the user to do the following

1. point it at 1 or more MARC files (either binary or MARCXML)
1. tell the application what type of MARC file it is (binary or MARCXML)
1. have the system convert all the MARC records into IIIF manifests with only the descriptive metadata defined.

This will require the following tool (which is out of scope of this product)

1. an application that will take the generated IIIF manifests and a location of digital files and add the matching files to each IIIF manifest thereby build the sequences for each manifest.

## Quickstart

```bash
$ git clone git@github.com:uchicago-library/marc2iiif
$ cd marc2iiif
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
```

PROTIP: if you are planning to add code to the library and want to be able to run tests without having to run install every time you test you can use

```python setup.py develop```

## Using the Library

```python

>>> from marc2iiif import MarcFilesFromDisk
>>> location = "/path/on/disk/to/a/directory/full/of/marc/records"
>>> marc_records = MarcFilesFromDisk(location)
>>> for record in marc_records:
>>>      print(record)

```

This will print out dictionaries for each marc record that was found in the path "/path/on/disk/to/a/directory/full/of/marc/records".

```python

>>> from marc2iiif import IIIFDataExtractionFromMarc
>>> from pymarc import MARCReader
>>> reader = MARCReader(open(marc_file_path), 'rb')
>>> record = None
>>> for rec in reader:
>>>     record = rec.as_dict()
>>> new_object = IIIFDataExtractionFromMarc.from_dict(record)

```

You now have a very a defined instance of a IIIFDataExtractionFromMarc object. You can get the name of the CHO that this record describes by entering

```python

>>> new_object.show_title()
'Jane\'s Wonderful Cultural Heritage Object'

```

Or, if you want the description of the CHO you can type

```python

>>> new_object.show_description()
'This is a description line composed of multiple description fields from MARC records'

```

If on the other hand you just want to know what metadata fields that were extracted from the inputted MARC record, you can type

```python

>>> new_object.show_metadata()
{
    "Added Entry - Personal Name": "Doe, Jane",
    "Edition Statement": "3rd"
}

```

Should you want to add additional metadata before you export your IIIF record, you can do the following

```python

>> new_metadata_field = {
    "field_name": "Production, Publication, Publication, Distribution, Manufacture, and Copyright Notice"
    "field_value": "2018 University of Chicago"
}
>>> new_object.add_metadata()

```

If you want to edit a particular metadata field or remove a particular metadata entry do the following:

```python

>>> new_object.modify_metadata({"Added Entry - Personal Name": "Doe, Jane"}, "Franklin, Diana")
>>> new_object.remove_metadata({"Added Entry - Personal Name": "Doe, Jane"})

```

If you want to change the title or description of the CHO then use these handy methods.

```python

new_object.change_title("New Title")
new_object.change_description("A totally new description that is way better than the old description")

```

## Contract for metadata labels

See [this wiki page](https://github.com/uchicago-library/marc2iiif/wiki/allow-metadata-field-names) for information about metadata field names to use when editing the metadata block.

And, check out [this wiki page](https://github.com/uchicago-library/marc2iiif/wiki/contract-example-for-dictionary-to-load-marc-records-into-IIIFDataExtractionFromMarc) for how to structure the dictionary passed to IIIFDataEXtractionFromMarc.from_dict() method.

## Additional Inforamtion

- [IIIF Presentation](http://iiif.io/api/presentation/2.1/)
- [MARC21](https://www.loc.gov/marc/bibliographic/)

## Author

- verbalhanglider (tdanstrom@uchicago.edu)