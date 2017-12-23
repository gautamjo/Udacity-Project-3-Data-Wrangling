# this code is written in python 3
import re

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
        correct_pin = "".join(pin_code.strip().split())

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