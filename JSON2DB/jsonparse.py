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


def create_table(objids, keyslist,valstr,  valnum,valbool):
    df = pd.DataFrame(columns=['objid', 'keystr', 'valstr', 'valnum','valbool'])
    df['objid'] = objids
    df['objid'].astype(int)
    df['keystr'] = keyslist
    df['valstr'] = valstr
    df['valbool'] = valbool
    df['valnum'] = valnum

    return df


def main(filepath):
    # 'test/test4/hard.json'
    with open(filepath, 'r')as f:
        data = json.load(f)

    pprint(data)
    # object id list, keys list, value list
    objids, keyslist, valslist = return_obj(data)

    # value type list
    valstr, valbool, valnum = val_type(valslist)

    # create schema
    df = create_table(objids, keyslist,valstr, valnum, valbool)
    pprint(df)
    base_name = str.rsplit(filepath, ".", 1)[0]
    df.to_csv(f'{base_name}.csv', index=False, header=False)


if __name__ == '__main__':
    main('test/test4/hard.json')
