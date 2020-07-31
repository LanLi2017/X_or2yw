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


def val_type(valslist):
    valstr = []
    valbool = []
    valnum = []
    for val in valslist:
        if isinstance(val, str):
            valstr.append(val)
            valbool.append(None)
            valnum.append(None)
        elif isinstance(val, bool):
            valbool.append(val)
            valstr.append(None)
            valnum.append(None)
        elif isinstance(val, (int,float)):
            valnum.append(val)
            valbool.append(None)
            valstr.append(None)
    print(valstr)
    print(valbool)
    print(valnum)
    return valstr,valbool,valnum


def create_table(objids, keyslist, valslist,valstr, valbool, valnum):
    df = pd.DataFrame(columns=['objid', 'keystr', 'valstr', 'valbool', 'valnum'])
    df['objid'] = objids
    df['objid'].astype(int)
    df['keystr'] = keyslist
    df['valstr'] = valstr
    df['valbool'] = valbool
    df['valnum'] = valnum

    return df


def main():
    with open('test/test4/hard.json', 'r')as f:
        data = json.load(f)

    pprint(data)
    objids, keyslist, valslist = return_obj(data)

    valstr, valbool, valnum = val_type(valslist)
    df = create_table(objids, keyslist, valslist,valstr, valbool, valnum)
    pprint(df)
    df.to_csv('test.csv', index=False)


if __name__ == '__main__':
    main()
