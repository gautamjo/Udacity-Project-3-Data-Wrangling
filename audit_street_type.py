# this code is written in python 3
import re
import mapping
from update_street_name import update_street_name

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

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