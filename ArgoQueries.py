import json
import random
import logging
import subprocess

import json2bulksql
from Global import argo_db, psql_db
from Query import Query
from JSON2DB import jsonparse
from Settings import ARGO_FILENAME, PSQL_USER, RESULTS_FILENAME, ARGO_PICKLE_FILENAME

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    with open(ARGO_PICKLE_FILENAME, 'rb') as infile:
        recommended_strings = json.load(infile)
except Exception as e:
    log.error("Couldn't find pickle file!! (exception: {0})".format(str(e)))
    recommended_strings = []


class PrepFilesArgo(Query):
    def __init__(self, filename):
        super().__init__("Preparing files for Argo consumption")
        self.filename = filename

    def db_command(self):
        # jsonparse.main(self.filename)
        json2bulksql.convertFile(self.filename, 0)


class Query1Argo(Query):
    def __init__(self):
        super().__init__("Projection Query 1")

    def db_command(self):
        return argo_db.execute_sql("SELECT * FROM argo_argo_data;")


class DropCollectionArgo(Query):
    def __init__(self):
        super().__init__("Dropping Data from Argo")

    def db_command(self):
        return argo_db.execute_sql("DELETE FROM argo")


class InitialLoadArgo(Query):
    def __init__(self):
        super().__init__("Loading Initial Data into Argo")

    def db_command(self):
        print("Starting...")
        PrepFilesArgo(ARGO_FILENAME).execute()
        data_copy_cmd = "\COPY argo_people_data(objid, keystr, valstr, valnum, valbool) FROM '{0}' WITH DELIMITER '|';".format(
            RESULTS_FILENAME)
        load_data = subprocess.Popen(["psql", "--password", "-U", PSQL_USER, "-d", "argo", "-c", data_copy_cmd],
                                     stdout=subprocess.PIPE)

        load_data.communicate()


def main():
    argo_loader = InitialLoadArgo()
    argo_loader.db_command()
    path = 'JSON2DB/test/test4/hard.csv'
    q1 = Query1Argo()
    res1 = q1.db_command()
    print(res1)


if __name__ == '__main__':
    main()