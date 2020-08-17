import glob
import json
import os
from pprint import pprint

import pymongo


def merge_data():
    # combine the provenance: JSON
    # path = f'../{args.log}/'
    path ='../log/'
    infiles = sorted(glob.glob(os.path.join(path, '*.json')), key=os.path.getmtime)

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
    return merge_data


def insert_data(merge_data, mycol):
    # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # mydb = myclient["firstdb"]
    # mycol = mydb["table1"]
    # with open('input.json', 'r')as f:
    #     data = json.load(f)
    x = mycol.insert_many(merge_data)
    print(x.inserted_ids)
    return mycol


def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["seconddb"]
    mycol = mydb["table2"]
    datas = merge_data()
    pprint(datas)
    mycol = insert_data(datas, mycol)
    for x in mycol.find():
        print(x)
    # print(mycol.find_one())


if __name__ == '__main__':
    main()