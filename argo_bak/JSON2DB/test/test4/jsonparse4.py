import json
from pprint import pprint
import pandas as pd
from pandas.core.computation.ops import isnumeric


def is_number(s):
    print(s)
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def recr_key_value(data, keys, vals, keystr, valstr):
    # use recursion to traverse all of the objects
    if isinstance(data, list):
        for i, v in enumerate(data):
            recr_key_value(v, keys, vals,f'{keystr}[{i}]', v)
    elif isinstance(data, dict):
        for key, value in data.items():
            if keystr:
                recr_key_value(value,keys, vals, f'{keystr}.{key}', value)
            else:
                recr_key_value(value, keys, vals, key, value)
    else:
        keys.append(keystr)
        vals.append(valstr)

    return keys, vals


def return_obj(data):
    # return
    # object id list
    # key list
    # value list
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


def create_table(objids, keyslist,valslist):
    df = pd.DataFrame(columns=['objid', 'keystr', 'valstr', 'valbool', 'valnum'])
    df['objid'] = objids
    df['objid'].astype(int)
    df['keystr'] = keyslist

    for i in range(len(valslist)):
        if isinstance(valslist[i], str):
            df.iloc[i]['valstr'] = valslist[i]
        elif isinstance(valslist[i], bool):
            df.iloc[i]['valbool'] = valslist[i]
        elif isinstance(valslist[i], (int, float)):
            df.iloc[i]['valnum'] = valslist[i]

    print(df)
    return df


def main():
    with open('hard.json', 'r')as f:
        data = json.load(f)

    pprint(data)
    # object id list, keys list, value list
    objids, keyslist, valslist = return_obj(data)

    # create schema
    df = create_table(objids, keyslist,valslist)
    # df.to_csv('test.csv', index=False)


if __name__ == '__main__':
    main()
