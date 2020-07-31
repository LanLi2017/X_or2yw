import json
from pprint import pprint


def recr_key_value(data, keys, vals, keystr, valstr):
    if isinstance(data, list):
        for i, v in enumerate(data):
            recr_key_value(v, keys, vals,f'{keystr}[{i}]', v)
    elif isinstance(data, dict):
        for key, value in data.items():
            if keystr:
                # keystr = f'{keystr}.{key}'
                recr_key_value(value,keys, vals, f'{keystr}.{key}', value)
            else:
                recr_key_value(value, keys, vals, key, value)
    else:
        keys.append(keystr)
        vals.append(valstr)

    return keys, vals


def return_objid(data):
    objids = []
    keys = []
    vals = []
    for i,v in enumerate(data):
        keystr = []
        valstr = []
        objectid = i
        keystr, valstr = recr_key_value(v,keystr, valstr,[],[])
        keys.extend(keystr)
        vals.extend(valstr)

        rep_t = len(keystr)
        objids.extend([objectid]*rep_t)
    return objids,keys,vals


def main():
    with open('hard.json', 'r')as f:
        data = json.load(f)

    pprint(data)
    # keys = []
    # vals = []
    # keys, vals = recr_key_value(data, keys,vals, [], [])
    # pprint(keys)
    # pprint(vals)
    objids, keyslist, valslist = return_objid(data)
    pprint(objids)
    pprint(keyslist)
    pprint(valslist)
    print(f'object ids length: {len(objids)}')
    print(f'keys length: {len(keyslist)}')
    print(f'value length: {len(valslist)}')


if __name__ == '__main__':
    main()
