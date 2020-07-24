import glob
import json
import os
import re

from Query.dependency import OPDependency


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


def return_colindex(datas, columns):
    data = datas[1]
    operation = data['operation']
    if operation['op'] == 'core/column-addition':
        column = operation['baseColumnName']
    else:
        column = operation['columnName']

    colidx = []
    if column in columns:
        for key,value in data.items():
            z = re.match(r'^\((\d+), (\d+)\)$', key)
            if z:
                print((int(z.group(1)), int(z.group(2))))
                colidx.append(int(z.group(2)))
    return list(set(colidx))


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
                    dep_dicts = OPDependency(data).mapping()
                    #  [{newcolumn: col}]
                    dependent_cols = []
                    for coldict in dep_dicts:
                        for gov,depend in coldict.items():
                            dependent_cols.append(depend)
                    colidx = []
                    for prev in prev_datas:
                        colidx = return_colindex(prev, dependent_cols)
                    res = extract_res(filename, value, row, column)
                    for idx in colidx:
                        cell_prov(prev_datas, row, idx, res)
                elif op == 'ColumnSplitChange':
                    columnindex = int(data['columnIndex'])
                    # print((row, columnindex))
                    res = extract_res(filename,value,row,column)
                    cell_prov(prev_datas, row, columnindex,res)
                    # res.append(cell_prov(prev_datas,row, columnindex))

                    # rigid transformation: prov = history, list_changes_cell()
                else:
                    res.extend(extract_res(filename,value,row, column))
    return res.sort(key=lambda x:x[0])


def main():
    path = '../../log4/'
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
    row = 2
    column = 4
    # # (2,4)
    res = []
    print(cell_prov(datas,row, column,res))


if __name__ == '__main__':
    main()
