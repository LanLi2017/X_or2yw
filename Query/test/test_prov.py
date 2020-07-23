import glob
import json
import os
from pprint import pprint

from dependency import OPDependency


def getvalue(data: str):
    if isinstance(data, dict):
        return data['v']
    else:
        try:
            value = json.loads(data)
            return value['v']
        except TypeError:
            return None


def extract_res(filename, value, row, column):
    res = []
    old_value = getvalue(value['old'])
    olddict = {old_value: (row, column)}
    new_value = getvalue(value['new'])
    newdict = {new_value: (row, column)}
    res.append((filename, olddict, newdict))
    return res


def cell_prov(datas, row, column, res):
    # what's the provenance for a single cell
    # rigid transformation || geometry transformation
    # add new column: self.prev_dep
    # dep: 'column name' || [{new: old}]
    # (row, dep_col)
    for d in datas:
        index = datas.index(d)
        data = d[1]
        filename = d[0]
        op = data['op']
        for key, value in data.items():
            if key == str((row, column)):
                prev_datas = datas[:index]
                # opd = OPDependency(data)
                # dep = opd.dep
                if op == 'ColumnAdditionChange':
                    # dep = {newcolumn: col}
                    pass
                elif op == 'ColumnSplitChange':
                    columnindex = int(data['columnIndex'])
                    # print((row, columnindex))
                    res = extract_res(filename,value,row,column)
                    cell_prov(prev_datas, row, columnindex,res)
                    # res.append(cell_prov(prev_datas,row, columnindex))

                    # rigid transformation: prov = history, list_changes_cell()
                else:
                    res.extend(extract_res(filename,value,row, column))
    return res


def main():
    path = '../../log5/'
    infiles = sorted(glob.glob(os.path.join(path, '*.json')), key=os.path.getmtime)
    filenames = []
    merge_data = []
    for infile in infiles:
        # find
        filep = os.path.splitext(infile)[0]
        filename = filep.split('/')[-1]
        filenames.append(filename)
        with open(infile) as f:
            data = json.load(f)
        merge_data.append(data)
    datas = list(zip(filenames, merge_data))
    row = 1
    column = 4
    # # (2,4)
    res = []
    res1 = cell_prov(datas,row, column,res)
    print(res1)


if __name__ == '__main__':
    main()
