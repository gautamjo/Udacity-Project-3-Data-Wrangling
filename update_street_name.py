# this code is written in python 3
import re

def update_street_name(name, mapping):
    """
    Return correct name if name is found in mapping dictionary. 
    Return name otherwise.
    """
    for key in mapping.keys():
        match = re.search(key, name) 
        if match:
            correct_name = re.sub(key, mapping[key], name)
            
            return correct_name.title()
        
    return name
                