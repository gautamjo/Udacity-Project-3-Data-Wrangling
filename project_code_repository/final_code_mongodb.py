# this code is written in python 3

import xml.etree.cElementTree as ET
import json
import re 
import mapping
from update_street_name import update_street_name

OSM_PATH = "new_delhi_sample.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# list of expected tags
CREATED = ["version", "changeset", "timestamp", "user", "uid"] 

# list of expected street names
expected = ['Delhi', 'Street', 'Nagar', 'Sadan', 'Marg', 'Road', 'Avenue', 'Circle', 'Mayur'
            'Place', 'Sector', 'Vihar', 'Enclave', 'Block', 'Chowk', 'Colony', 'Mandir', 'Market', 'Place', 'Lane',
            'Estate', 'Bazaar', 'Kunj', 'Circus', 'Extension', 'College', "Paharganj", "Janakpuri", "Flat", "Palika", 
            'Gate']

MAPPING = mapping.mapping
                
def audit_street_type(street_name):
    """
    Return updated street name if name is not in expected street name list. 
    Return street name otherwise.
    """
    match = street_type_re.search(street_name)
    if match:
        street_type = match.group()
        if street_type not in expected:
            return update_street_name(street_name, MAPPING)
    
    return street_name

def is_street_name(elem):
    """Return True if the value of two operands are equal. Return False otherwise."""
    return elem.attrib['k'] == "addr:street"

# functions that deal with post codes
invalid_pins = []
def pin_validator(pin):
    """
    Return a pin if pin code is 6 digit valid pin. Else append invalid pin codes to a list.
    """
    pin_validator = re.compile(r'^[1-9][0-9]{5}$') 
    match = pin_validator.search(pin)
    if match:
        correct_pin = pin

        return correct_pin
    
    invalid_pins.append(pin)
    #return pin

def simple_pin_code_fix(pin_code):
    """
    Return a corrected pin code if a wrong pin code is found. Else return just the pin code.
    This is not a generalized solution. It fixes only the wrong pin codes of this dataset.
    """
    pin = list(pin_code)
    
    if len(pin) > 6 and pin_code.count("0") > 3:
        pin.remove("0")
        correct_pin = "".join(pin)

        return correct_pin

    elif len(pin) > 6 and pin_code.count(" ") > 0:
        pin.remove(" ")
        correct_pin = "".join(pin)

        return correct_pin

    elif pin_code.startswith("10", 0, 2):
        correct_pin = re.sub(r"^10", "11", pin_code)

        return correct_pin
    
    elif pin_code.endswith("0", -1) and pin_code.startswith("2", 0) and len(pin) > 6:
        del pin[-1]
        correct_pin = "".join(pin)
        
        return correct_pin
    
    return pin_code

def is_pin_code(elem):
    """Return True if the value of two operands are equal. Return False otherwise."""
    return elem.attrib["k"] == "addr:postcode"

# this function deals with phone numbers
def is_phone_number(elem):
    """
    Return True if the value of the operands are equal. Return False otherwise.
    """
    return elem.attrib["k"] == "phone"

def phone_fixer(phone):
    """
    Return a phone number after striping its whitespaces or non-digit characters except "+" (plus symbol). 
    """
    phone_num = phone
    join_num = "".join(phone_num.strip().split())
    match_num = re.search(r"[^\d+]", join_num)
    if match_num:
        fix_num = re.sub(match_num.group(), "", join_num)
        
        return fix_num
    
    return join_num

def shape_element(elem):
    """Clean and shape node or way XML element to Python dict"""
    if elem.tag == "node" or elem.tag == "way":
        nodes = {"created": {}, "type" : elem.tag} # dictionary that will store attributes and their values
        if "lat" in elem.attrib and "lon" in elem.attrib:
                nodes["pos"] = [float(elem.attrib["lat"]), float(elem.attrib["lon"])]
        
        for tag in elem.attrib:
            if tag == "lat" or tag == "lon":
                continue
            elif tag in CREATED:
                nodes["created"][tag] = elem.attrib[tag]
            else:
                nodes[tag] = elem.attrib[tag]
        
        for data in elem.iter("tag"):
            match = PROBLEMCHARS.search(data.attrib["k"])
            if match:
                continue
            elif LOWER_COLON.match(data.attrib['k']):
                address = data.attrib["k"].split(":", 2)  
                if len(address) == 2:
                    if "address" not in nodes:
                        nodes["address"] = {}
                    elif is_street_name(data):
                        nodes["address"][address[1]] = audit_street_type(data.attrib["v"])
                    elif is_pin_code(data):
                        nodes["address"][address[1]] = pin_validator(simple_pin_code_fix(data.attrib["v"]))
            else:
                if is_phone_number(data):
                    nodes[data.attrib["k"]] = phone_fixer(data.attrib["v"])
                else:
                    nodes[data.attrib["k"]] = data.attrib["v"]
        
        node_ref = []        
        for nd_tag in elem.iter("nd"):
            node_ref.append(nd_tag.attrib["ref"])
        
        if len(node_ref) > 0:
            nodes["node_ref"] = node_ref
        
        return nodes
    else:
        
        return None
            
def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data

if __name__ == '__main__':
    process_map(OSM_PATH)