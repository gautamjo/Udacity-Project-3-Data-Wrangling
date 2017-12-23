
# This code is written in python 3
import operator
import xml.etree.cElementTree as ET

def count_tags(file):
    """
    Return a list of tuples with tag names and tag count found in an OSM file.
    """
    tags = {}
    for event, element in ET.iterparse(file):
        tags[element.tag] = tags.get(element.tag, 0) + 1
    
    # sorting tags by values. 
    sorted_tags = sorted(tags.items(), key=operator.itemgetter(1))
    # returns a sorted representation of tags that will be a list of tuples.
    return sorted_tags