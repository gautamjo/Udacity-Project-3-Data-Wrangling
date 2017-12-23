# this code is written in python 3
import xml.etree.cElementTree as ET

def process_map(file):
    """
    Return a set of unique users.
    """
    users = set()
    for event, element in ET.iterparse(file):
        if 'uid' in element.attrib:
            users.add(element.attrib['uid'])

    return users

def test(file):
    user = process_map(file)
    print("Number of unique users:", len(user))

