import json
from pprint import pprint

with open('simple.json', 'r')as f:
    data = json.load(f)

pprint(data)
keystr = []
valstr = []

for key, value in data.items():
    print(f'{key} -> {value}')

