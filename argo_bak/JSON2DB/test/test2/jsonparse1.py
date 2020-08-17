import json
from pprint import pprint

with open('med.json', 'r')as f:
    data = json.load(f)

pprint(data)
keystr = []
valstr = []

for key, value in data.items():
    if isinstance(value, list):
        for i, v in enumerate(value):
            keystr.append(f'{key}[{i}]')
            valstr.append(v)

        print('hahah')
    else:
        print(f'{key} -> {value}')
        keystr.append(key)
        valstr.append(value)

pprint(keystr)
pprint(valstr)
