[![Build Status](https://travis-ci.org/uchicago-library/marc2iiif.svg?branch=master)](https://travis-ci.org/uchicago-library/marc2iiif) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/marc2iiif/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/marc2iiif?branch=master)
# Introduction

This is an application that will allow the user to do the following

1. point it at 1 or more MARC files (either binary or MARCXML)
1. tell the application what type of MARC file it is (binary or MARCXML)
1. have the system convert all the MARC records into IIIF manifests with empty sequences and filled-in descriptive metadata


This will require the following tool (which is out of scope of this product)

1. an application that will take the generated IIIF manifests and a location of digital files and add the matching files to each IIIF manifest thereby filling in the sequence

# marc2iiif
An application that will take 1 or more Marc records (in either binary or MARCXML) and convert them into IIIF manifests
