# this code is written in python 3
import re

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