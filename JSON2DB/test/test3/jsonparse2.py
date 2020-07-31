import json
from pprint import pprint


def recr_key_value(data, keys, vals, keystr, valstr):
    if isinstance(data, list):
        for i, v in enumerate(data):
            recr_key_value(v, keys, vals,f'{keystr}[{i}]', v)
    elif isinstance(data, dict):
        for key, value in data.items():
            if keystr:
                keystr = f'{keystr}.{key}'
                recr_key_value(value,keys, vals, keystr,value)
            else:
                recr_key_value(value, keys, vals, key, value)
    else:
        keys.append(keystr)
        vals.append(valstr)

    return keys, vals


def main():
    with open('med1.json', 'r')as f:
        data = json.load(f)

    pprint(data)
    keys = []
    vals = []
    keys, vals = recr_key_value(data, keys,vals, [], [])
    pprint(keys)
    pprint(vals)


if __name__ == '__main__':
    main()
