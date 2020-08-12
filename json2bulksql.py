#!/usr/bin/env python

import sys
import string
import optparse

import ijson as ijson

try:
    import json
except ImportError:
    import simplejson as json


class SingleTableBulkSQLFileWriterObjectHandler(object):
    def __init__(self, outfile):
        self.outfile = outfile

    def handleInternal(self, objid, key, obj):
        if isinstance(obj, str):
            print(str(objid) + "|" + key + "|" + obj + "|\\N|\\N", file=self.outfile)
        elif isinstance(obj, bool):
            if (obj):
                print(str(objid) + "|" + key + "|\\N|\\N|1", file=self.outfile)
            else:
                print(str(objid) + "|" + key + "|\\N|\\N|0", file=self.outfile)
        elif isinstance(obj, int) or isinstance(obj, float):
            print(str(objid) + "|" + key + "|\\N|" + str(obj) + "|\\N", file=self.outfile)
        elif isinstance(obj, list):
            for (idx, list_item) in enumerate(obj):
                self.handleInternal(objid, key + ":" + str(idx), list_item)
        elif isinstance(obj, dict):
            if len(key) > 0:
                prekey = key + "."
            else:
                prekey = ""
            for (subkey, subval) in obj.items():
                self.handleInternal(objid, prekey + subkey, subval)

    def handle(self, obj, objid, last=False):
        self.handleInternal(objid, "", obj)


def convertFile(input_filename, start_objid=0):
    infile = open(input_filename, 'r')
    # collection = json.load(infile)

    basename = str.rsplit(input_filename, ".", 1)[0]
    print(basename)

    outfile = open(basename + ".txt", 'w')

    writer = SingleTableBulkSQLFileWriterObjectHandler(outfile)
    infile.seek(0)
    parser = ijson.items(infile, "item")
    for (objid, item) in enumerate(parser):
        writer.handle(item, objid + start_objid)

    outfile.close()


def main(filename="JSON2DB/test/test4/hard.json"):

    # convertFile(input_filename, start_objid=0, show_pbar=False, single_table=False):
    with open(filename, 'r')as f:
        data = json.load(f)
        print(data)
    convertFile(filename, 0)


if __name__ == "__main__":
    main()
