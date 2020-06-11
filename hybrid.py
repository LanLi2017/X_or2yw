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


def unzip(rootPath, pattern):
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
            extract_p = os.path.join(root, os.path.splitext(filename)[0])
            zipfile.ZipFile(os.path.join(root, filename)).extractall(extract_p)


def pair_recipe_history(rootPath, path):
    ''' extract op from data.txt'''
    with open(path, 'r')as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    idx = 0
    # start = 0
    # end = 0
    historypath = str()
    while idx < len(data):
        line = data[idx]
        if re.match(r'^pastEntryCount=\d+$', line):
            pastEntryCount = int(line.rsplit('=',1)[1])
            jsonfiles = data[idx+1: idx+1+pastEntryCount]
            for jsonfile in jsonfiles:
                file = json.loads(jsonfile)
                # pairing
                historyid = file['id']
                historypath = f'{rootPath}/history/{historyid}.change/change.txt'
                with open(historypath, 'r')as fout:
                    data = fout.readlines()
                pprint(data)
            idx +=1
        idx += 1


def extract_history(history_path):
    ''' '''
    pass


def main():
    # args: root path
    rootPath = r"1660451457167.project"
    # zip history pattern
    zip_his_pattern = '*.change.zip'
    # zip data pattern
    zip_data_pattern = '*.zip'

    # unzip
    # unzip(rootPath, zip_his_pattern)
    # unzip(rootPath, zip_data_pattern)

    # history pattern
    # his_pattern = f'{rootPath}/*.change/change.txt'
    # print(his_pattern)
    # infiles = glob.glob(his_pattern)
    # print(infiles)

    # data pattern
    data_path = f'{rootPath}/data/data.txt'
    pair_recipe_history(rootPath,data_path)

    # extract_history(history_path)


if __name__ == '__main__':
    main()