# unzip
# path
# id pairing
import fnmatch
import glob
import json
import os
import re
import zipfile
from pprint import pprint

import Options
from parse_orhistory import parse_txt
from parse_orhistory.parse_txt import func_map, name_map


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
                # try:
                #     colname = file['operation']['columnName']
                #
                # except:
                #     colname = file['operation']['newColumnName']
                # else:
                #     pass
                # for d in colindx:
                    # colmodel = json.loads(d)
                # file['oldColumn']['cellIndex']
                # operation = file['operation']
                # if operation['op'] == 'core/column-removal':
                    # oldCol = json.loads(file['oldColumn'])
                    # cellIndex = int(oldCol['cellIndex'])
                    # file.update({'cellindex': cellIndex})
                    # index should be captured in change.txt
                #     pass
                # else:
                #     for d in colindx:
                #         colmodel = json.loads(d)
                #         if colmodel['name'] == colname:
                #             file.update({'cellindex': colmodel['cellIndex']})
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

                prov_path = f'{log}/hybrid{index}.json'
                with open(prov_path, "w") as fout:
                    json.dump(file, fout, indent=4)

            idx +=1
        idx += 1

    return file


def extract_history(history_path):
    ''' '''
    pass


def main():

    # args: root path
    args = Options.get_args()

    rootPath = args.root_path
    # rootPath = r"1660451457167.project"

    # zip history pattern
    zip_his_pattern = '*.change.zip'
    # zip data pattern
    zip_data_pattern = '*.zip'

    # unzip
    unzip(rootPath, zip_his_pattern)
    unzip(rootPath, zip_data_pattern)

    # history pattern
    # his_pattern = f'{rootPath}/*.change/change.txt'
    # print(his_pattern)
    # infiles = glob.glob(his_pattern)
    # print(infiles)
    # log_folder = 'log'
    log_folder = args.log
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # data pattern
    data_path = f'{rootPath}/data/data.txt'
    pair_recipe_history(rootPath,data_path, log_folder)

    # extract_history(history_path)


if __name__ == '__main__':
    main()