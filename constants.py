import json
import dataset
import re
from random import choice
from datetime import datetime, timedelta

red = 0xff4e3d
maroon = 0xc0291b

# Get json file of strings
with open('strings.json', 'r') as strings_file:  
    strings = json.load(strings_file)

# Get database
db = dataset.connect('sqlite:///database.db')
autorole_db = db.get_table('autorole', primary_id='id')

def log(content):
    print('{} {}'.format(datetime.now(), content))

def pop_flags(args):
    """Returns (flags, args for flag). Flags are words starting with -"""
    split_on_flags = ' '.join(list(args)).split('-')
    del split_on_flags[0]
    flags = []
    flag_args = []
    for flag_group in split_on_flags:
        flag_group_list = flag_group.split(' ')
        flag = flag_group_list.pop(0)
        flags.append(flag)
        flag_args.append(' '.join(flag_group_list))
    return (flags, flag_args)


_separator = ', '

def list_to_string(_list):
    return _separator.join(_list)

def string_to_list(_string):
    return _string.split(_separator)

def string_to_dict(_string):
    d = dict()
    for entry in re.split('[\s,]', _string):
        (key, val) = tuple(re.split('[=]', entry))
        d[key] = val
    return d