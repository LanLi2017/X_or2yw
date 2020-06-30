# cell at row * column *, what's the function ?
# cell at row * column *, what're the changes?
# given row index, column index, return cell workflow
import glob
import json
import operator
import os

import Options


def getvalue(data: str):
    if isinstance(data, dict):
        return data['v']
    else:
        try:
            value = json.loads(data)
            return value['v']
        except TypeError:
            return None


# trace from JSON file, and query
def count_change_cells():
    # query: how many cells have been changed in total

    pass


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
                res.append((filename, data['operation']['op']))

    return res


def count_change_cell(row, column, datas):
    # query: how many changes applied on one single cell
    changes = list_changes_cell(row, column, datas)
    return len(changes)


def count_op_cell(row, column, datas):
    # how many operations applied on one single cell
    res = list_operations(datas,column, row)
    return len(res)


def cell_dep():
    pass


def most_changes(data: dict):
    # query: which operation in which step changes the most cells value?
    # opname = 'single-edit'
    # if data['operations']['op']:
    #     opname = data['operations']['op']
    desc = data['operation']['description']
    count_changes = 0
    # column additon newCellCount ; rename:
    if data['op'] == 'ColumnAdditionChange':
        count_changes = data['newCellCount']
    elif data['op'] == 'ColumnRemovalChange':
        count_changes = data['oldCellCount']
    elif data['op'] == 'MassCellChange':
        count_changes = data['cellChangeCount']
    elif data['op'] == 'ColumnSplitChange':
        new_col = int(data['columnNameCount'])
        new_row = int(data['rowIndexCount'])
        if data['removeOriginalColumn'] == 'false':
            count_changes = new_col * new_row
        elif data['removeOriginalColumn'] == 'true':
            cellChangeCount = int(data['cellChangeCount'])
            count_changes = new_col * new_row + cellChangeCount
    elif data['op'] == 'CellChange':
        count_changes = 1
    elif data['op'] == 'ColumnRenameChange':
        # rename operation has no value change
        count_changes = 0
    else:
        count_changes = 0
    # res = {desc: count_changes}
    return count_changes, desc


def main():
    # args
    args = Options.get_args()
    row = args.row
    column = args.column

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
    datas = zip(filenames, merge_data)

    # return choice: 1. operations 2. cell changes
    if return_command == 'changes':
        res = list_changes_cell(row, column, datas)
    elif return_command == 'operations':
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
    elif return_command == 'count-changes':
        res = count_change_cell(row, column, datas)
    elif return_command == 'count-operation':
        res = count_op_cell(row, column, datas)

    # output = f'result/{args.out}'
    # log_folder = 'result/'
    log_folder = args.out
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    if return_command == 'most-value-changes':
        output = f'{log_folder}/{return_command}.txt'
    else:
        output = f'{log_folder}/{return_command}_row{args.row}_column{args.column}.txt'
    with open(output, 'w')as file:
        file.write(str(res))
    return res


if __name__ == '__main__':
    main()
