"""utility functions for marc2iiif library
"""

from sys import stderr

def match_single_file(src, pot_match=None):
    if pot_match:
        if src == pot_match:
            return True
    return False

def search_for_marc_file(src, pot_match=None):
    """a function to determine if a file in a directory tree is a MARC record

    :param str src: an absolute filepath to a file that may be a MARC record

    :rtype Boolean
    """
    if src.endswith('mrc'):
        return True
    else:
        return False


def default_identifier_extraction(value):
    """a function to take a pi.lib URL and return the unique identifier 
    
    It splits the URL from the scheme and host name. WARNING: assumes that the scheme is
    https which is hard-coded into the string

    :param str value: a pi.lib.uchicago.edu URL string

    :rtype str
    """
    if 'http' in value:
        items = value.split("http://pi.lib.uchicago.edu/1001/")
    elif 'https' in value:
        items = value.split("https://pi.lib.uchicago.edu/1001/")
    else:
        items = []
        stderr.write("{} is not a valid URL".format(value))
    if len(items) == 2:
        out = (True, items[1])
    else:
       out = (False, None)
    return out

def combine_subfields_into_one_value(list_of_dicts):
    single_string = ""
    for a_dict in list_of_dicts:
        single_string += " " + a_dict.get(list(a_dict.keys())[0])
    return single_string.strip()
 