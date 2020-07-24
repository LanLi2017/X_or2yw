# cell at row * column *, what's the function ?
# cell at row * column *, what're the changes?
# given row index, column index, return cell workflow
import glob
import json
import os
import re

import Options
import pandas as pd

# from dependency import OPDependency
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


def list_changes_cell(row, column, datas):
    # query: what the changes applied on this cell?
    res = []
    for d in datas:
        data = d[1]
        filename = d[0]
        op = data['op']
        for key, value in data.items():
            if key == str((row, column)):
                if op == 'ColumnRemovalChange':
                    res.append((filename, value))
                else:
                    old_value = getvalue(value['old'])
                    olddict = {old_value: (row, column)}
                    new_value = getvalue(value['new'])
                    newdict = {new_value: (row, column)}
                    res.append((filename, olddict, newdict))
    return res


def list_operations(datas, column, row):
    # query: what the operations applied on this cell
    # column level / cell-level
    # split column : apply on some column, but get changes on other column
    # can not set row column at the same time, because it might has no changes
    res = []
    for d in datas:
        data = d[1]
        filename = d[0]
        if data['op'] == 'CellChange':
            for key, value in data.items():
                if key == str((row, column)):
                    res.append((filename, 'single-edit'))
        elif data['op'] == 'ColumnSplitChange':
            if column in data['cellidx_list']:
                res.append((filename, data['operation']['op']))
        else:
            if column == data['cellindex']:
                # res.append((filename, data['operation']['op']))
                res.append((filename, data['description']))

    return res


def get_ori_value(curdata, row, column, datas):
    # query: # what's the original value of a single cell (row, column)?
    changed_cell_list = list_changed_cells(datas)
    # if the (row, column) is not in all of cells which get changed, return the current value
    # include not changed & applied op but not changed
    if (row, column) in changed_cell_list:
        # invoke changes-single-cel function: provenance of cell change
        list_changes = list_changes_cell(row, column, datas)
        # [('hybrid1', {None: (1, 30)}, {None: (1, 30)}), ('hybrid3', {'old': '', 'new': None}), ('hybrid4', {None: (1, 30)}, {'Lincoln Park Oasis  Unit 2 ONLY': (1, 30)})]
        # back to the first tuple: ('hybrid1', {None: (1, 30)}, {None: (1, 30)})
        first_step = list_changes[0]
        ori_value = first_step[1].keys()
        return ori_value
    else:
        return curdata.iat[row,column]


def count_change_cells(op):
    # return the total number of changes for each operation
    count = 0
    for key, value in op.items():
        z = re.match(r'^\((\d+), (\d+)\)$', key)
        if z:
            count +=1
    return count


def count_change_cell(row, column, datas):
    # query: how many changes applied on one single cell
    changes = list_changes_cell(row, column, datas)
    return len(changes)


def count_op_cell(row, column, datas):
    # how many operations applied on one single cell
    res = list_operations(datas,column, row)
    return len(res)


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
    res.sort(key=lambda x: x[0])
    return res


def list_changed_cells(datas):
    # query: what are the cells get actual changes?
    res = []
    for d in datas:
        data = d[1]
        for key,value in data.items():
            z = re.match(r'^\((\d+), (\d+)\)$', key)
            if z:
                res.append((int(z.group(1)), int(z.group(2))))
    # return list of changed cell at (row, column)
    # remove duplicates
    return list(set(res))


def count_changed_cells(datas):
    # how many cells have been changed
    res = list_changed_cells(datas)
    return len(res)


def most_changes(data: dict):
    # query: which operation in which step changes the most cells value?
    # opname = 'single-edit'
    # if data['operations']['op']:
    #     opname = data['operations']['op']
    desc = data['operation']['description']
    # count_changes = 0
    count_changes = count_change_cells(data)
    # column additon newCellCount ; rename:
    # if data['op'] == 'ColumnAdditionChange':
    #     count_changes = data['newCellCount']
    # elif data['op'] == 'ColumnRemovalChange':
    #     count_changes = data['oldCellCount']
    # elif data['op'] == 'MassCellChange':
    #     count_changes = data['cellChangeCount']
    # elif data['op'] == 'ColumnSplitChange':
    #     new_col = int(data['columnNameCount'])
    #     new_row = int(data['rowIndexCount'])
    #     if data['removeOriginalColumn'] == 'false':
    #         count_changes = new_col * new_row
    #     elif data['removeOriginalColumn'] == 'true':
    #         cellChangeCount = int(data['cellChangeCount'])
    #         count_changes = new_col * new_row + cellChangeCount
    # elif data['op'] == 'CellChange':
    #     count_changes = 1
    # elif data['op'] == 'ColumnRenameChange':
    #     # rename operation has no value change
    #     count_changes = 0
    # elif data['op'] == 'MassRowColumnChange':
    #     # transpose
    #     count_changes = count_change_cells(data)
    # else:
    #     ''' transpose need to be constructed '''
    #     count_changes = 0
    # res = {desc: count_changes}
    return count_changes, desc


def main():
    # args
    args = Options.get_args()
    row = args.row
    column = args.column
    # get dataframe current dataset
    data_path = f'.././data/{args.data}'
    cur_data = pd.read_csv(data_path,index_col=False)

    # row = 2
    # column = 1

    path = f'../{args.log}/'
    # path ='../log/'
    infiles = sorted(glob.glob(os.path.join(path, '*.json')), key=os.path.getmtime)

    # ask what?
    return_command = args.command
    # return_command = 'changes'
    # return_command = 'operations'
    res = []

    # filenames: data
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

    # return choice: 1. operations 2. cell changes
    if return_command == 'changes-single-cell':
        res = list_changes_cell(row, column, datas)
    elif return_command == 'operations-single-cell':
        # need to change: operation name might not tell anything
        res = list_operations(datas,column, row)
    elif return_command == 'most-value-changes':
        # for column addition: newCellCount
        # for column removal: oldCellCount
        # for single edit: default: 1
        # how many value changes?
        max_count = 0
        max_desc = ''
        for d in datas:
            data = d[1]
            filename = d[0]
            count_desc = most_changes(data)
            count = int(count_desc[0])
            desc = count_desc[1]
            if count > max_count:
                max_count = count
                max_desc = desc
            res = [filename, max_count, max_desc]
    elif return_command == 'count-changes-single-cell':
        res = count_change_cell(row, column, datas)
    elif return_command == 'count-operation-single-cell':
        #
        res = count_op_cell(row, column, datas)
    elif return_command == 'reverse-data':
        res = get_ori_value(cur_data,row, column, datas)
    elif return_command == 'list-changed-cells':
        res = list_changed_cells(datas)
    elif return_command == 'count-changed-cells':
        res = count_changed_cells(datas)
    elif return_command == 'prov-single-cell':
        res = cell_prov(datas, row, column, res)
    elif return_command == 'merge':
        # output queries in batch
        result = []
        res = {}
        res['List all of changes applied on this cell']= list_changes_cell(row, column, datas)
        res['List all of operations applied on this cells'] = list_operations(datas,column,row)
        res['Count how many changes applied on this cell'] = count_change_cell(row,column,datas)
        res['Count how many operations applied on this cell'] = count_op_cell(row, column, datas)
        res['Reverse the data cleaning task and return the original cell value'] = get_ori_value(cur_data, row,column,datas)
        res['List all of the cells which get changed'] = list_changed_cells(datas)
        res['Count how many cells have been changed'] = count_changed_cells(datas)
        res['Provenance of this single cell'] = cell_prov(datas,row,column,result)

    # output = f'result/{args.out}'
    # log_folder = 'result/'
    log_folder = args.out
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    if return_command == 'most-value-changes':
        output = f'{log_folder}/{return_command}.txt'
    elif return_command == 'list-changed-cells':
        output = f'{log_folder}/{return_command}.txt'
    else:
        output = f'{log_folder}/{return_command}_row{args.row}_column{args.column}.txt'

    with open(output, 'w')as file:
        if isinstance( res, list):
            for r in res:
                file.write(str(r)+'\n')
        elif isinstance(res, dict):
            for r in res.items():
                file.write(str(r)+'\n')
        # json.dump(res, file, indent=2, sort_keys=True)

    return res


if __name__ == '__main__':
    main()
