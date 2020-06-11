# unzip
# path
# id pairing
import fnmatch
import glob
import os
import zipfile


def unzip(rootPath, pattern):
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
            extract_p = os.path.join(root, os.path.splitext(filename)[0])
            zipfile.ZipFile(os.path.join(root, filename)).extractall(extract_p)


def extract_op(path):
    ''' extract op from data.txt'''

    pass


def extract_history(history_path):
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
    extract_op(data_path)

    # extract_history(history_path)


if __name__ == '__main__':
    main()