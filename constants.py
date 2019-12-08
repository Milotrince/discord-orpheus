import json

red = 0xdd3300

# Get json file of strings
with open('strings.json', 'r') as strings_file:  
    strings = json.load(strings_file)