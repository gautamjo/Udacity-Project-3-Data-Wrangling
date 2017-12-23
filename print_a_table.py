# this code is written in python 3
import os
from prettytable import PrettyTable as PT
def get_filesize(filename):
	"""
	Return the byte size of a filename.
	"""
	return os.path.getsize(filename)

def convert_bytes(file):
    """
    Return filesize in bytes converted to KB, MB, GB, TB 
    """
    size = ['bytes', 'KB', 'MB', 'GB', 'TB']
    for x in size:
        if file < 1024.0:
            return "{:.1f} {}".format(file, x)
        file /= 1024.0

def pt_table(fields, items):
    """
    Prints the data in tabular from.
    """
    table = PT(fields, header_style='upper')
    for i in items:
        table.add_row(i)
        
    print(table)