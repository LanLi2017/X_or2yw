# unzip
# path
# id pairing
import fnmatch
import json
import os
import re
import zipfile
from pprint import pprint

from archive_query import Options
from parse_orhistory.parse_txt import func_map, name_map
import pandas as pd


def create_folder(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)


def unzip(rootPath, pattern):
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
            extract_p = os.path.join(root, os.path.splitext(filename)[0])
            zipfile.ZipFile(os.path.join(root, filename)).extractall(extract_p)


def pair_recipe_history(rootPath, path, log):
    ''' extract op from data.txt'''
    with open(path, 'r')as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    idx = 0
    # start = 0
    # end = 0
    file = dict()
    # colindx = []
    while idx < len(data):
        line = data[idx]
        # if re.match(r'^columnCount=\d+$', line):
        #     columncount = int(line.rsplit('=',1)[1])
        #     colindx = data[idx+1: idx+1+columncount]

        if re.match(r'^pastEntryCount=\d+$', line):
            pastEntryCount = int(line.rsplit('=',1)[1])
            jsonfiles = data[idx+1: idx+1+pastEntryCount]
            index = 0
            for jsonfile in jsonfiles:
                index +=1
                file = json.loads(jsonfile)
                # pairing
                historyid = file['id']
                historypath = f'{rootPath}/history/{historyid}.change/change.txt'
                with open(historypath, 'r')as fout:
                    data = fout.readlines()
                data = [x.strip() for x in data]
                opname = data[1].split('.')[-1]
                top_count = name_map[opname]
                head, top, content = data[0], data[1:top_count + 1], data[top_count + 1:]
                op = func_map[opname](top, content)
                file.update(op)
                add_signature(file)

                prov_path = f'{log}/hybrid{index}.json'
                with open(prov_path, "w") as fout:
                    json.dump(file, fout, indent=4)

            idx +=1
        idx += 1
    return file


def refine_cells(cells:list):
    # cells: [{"v":"laura"},{"v":2070},{"v":" LAURA"},{"v":" GREY"},{"v":"user"}]
    res = []
    for cell in cells:
        if cell:
            value = cell['v']
            # pprint(value[0])
        else:
            # if the values of the whole column are null
            value = cell
        res.append(value)
    return res


def extract_data(data_path):
    ''' '''
    ''' extract current dataset from data.txt'''
    with open(data_path, 'r')as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    idx = 0
    # current dataset
    dataset = []
    # column metadata
    columnmodel = {}

    while idx < len(data):
        line = data[idx]

        # column model: get column
        if re.match(r'^columnCount=\d+$', line):
            columncount = int(line.rsplit('=',1)[1])
            colindx = data[idx+1: idx+1+columncount]
            for col in colindx:
                colmodel = json.loads(col)
                cellindex = int(colmodel['cellIndex'])
                name = colmodel['name']
                columnmodel.update({cellindex: name})
            idx += 1
        if re.match(r'^rowCount=\d+$', line):
            dataset = data[idx + 1: len(data)]
            idx +=1
        idx +=1
    # initialize column index, create dataframe
    # df = {}
    df = []
    for d in dataset:
        d_load = json.loads(d)
        cells = d_load['cells']
        refinecells = refine_cells(cells)
        df.append(refinecells)
        # df.update({columnmodel[col]: refinecells})

    dataframe = pd.DataFrame(df)
    # column model :
    # {0: 'Login email', 1: 'Identifier', 4: 'group', 2: 'First name', 3: 'Last name'}
    # remove "removing" column
    dataframe = dataframe.dropna(axis=1, how='all')
    pprint(dataframe)
    dataframe.columns = [cell[1] for cell in sorted(columnmodel.items())]
    return dataframe


def add_signature(datas):
    ''' row: i, column: j  apply unique signature for each cell
        s = 2^i * 3^j
        the history of signature should be history/life of this cell
    '''
    sig = dict()
    for key, value in datas.items():
        z = re.match(r'^\((\d+), (\d+)\)$', key)
        if z:
            row = int(z.group(1))
            column = int(z.group(2))
            # calculate unique signature
            s = pow(2, row) * pow(3, column)
            sig['signature'] = s
            value.update(sig)
    return datas


def main():

    # args: root path
    args = Options.get_args()

    rootPath = args.root_path
    # rootPath = r'1827202584598.project'
    # rootPath = r"1660451457167.project"

    # zip history pattern
    zip_his_pattern = '*.change.zip'
    # zip data pattern
    zip_data_pattern = '*.zip'

    # unzip
    unzip(rootPath, zip_his_pattern)
    unzip(rootPath, zip_data_pattern)

    # history pattern
    # his_pattern = f'{rootPath}/*.change/transpose_chan.txt'
    # print(his_pattern)
    # infiles = glob.glob(his_pattern)
    # print(infiles)
    # log_folder = 'log'
    log_folder = args.log
    # log_folder = 'log8'
    create_folder(log_folder)

    # data pattern
    data_path = f'{rootPath}/data/data.txt'
    # data_path = '1827202584598.project/data/data.txt'

    # dataframe = extract_data(data_path)
    # savedata = args.data
    # create_folder(savedata)
    # cur_dataname = rootPath.split('.')[0]
    # dataframe.to_csv(f'{savedata}/{cur_dataname}_clean.csv', index=False)

    # pairing history and data
    pair_recipe_history(rootPath,data_path, log_folder)
    # extract_history(history_path)


if __name__ == '__main__':
    main()