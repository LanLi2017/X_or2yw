import glob
import json
import os
from pprint import pprint

import pymongo


def query1_prov(mycol, hid):
    # given history id; return prov
    res = []
    for x in mycol.find({"id": hid}):
        res.append(x)
    pprint(res)
    return res


def query2(mycol):
    # return all of the changes on row 0, column 0
    # res = mycol.find_one(projection={'"(0, 1)"': True})
    res = []
    for ans in mycol.find(projection={'"(0, 1)"': True}):
        print(ans)
    print(res)
    return res
    pass


def query3_count():
    # count how many changes
    pass


def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["seconddb"]
    mycol = mydb["table2"]
    # pprint(mycol.find_one())
    query1_prov(mycol, 1591902583373)


if __name__ == '__main__':
    main()

