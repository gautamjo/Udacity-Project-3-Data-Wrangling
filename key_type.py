
# this code was written in python 3
import re
import xml.etree.cElementTree as ET

lower = re.compile(r'^([a-z]|_)*$') # value that contain only lowercase letters
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$') # for value with a colon in its name
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]') # for value that might have a problem (whitespace, special characters and such)

def key_type(element, keys):
    """
    Return a dictionary keys with updated values if those values are found in an element.
    """
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            if lower.search(k):
                keys['lower'] += 1
            elif lower_colon.search(k):
                keys['lower_colon'] += 1
            elif problemchars.search(k):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
    
    return keys

def process_map(filename):
    """Return a dictionary named keys with updated values if those values are in filename.
    """
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0} # container for values found in the "k" attribute
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

