import logging
import subprocess
from pprint import pprint

from argo_bak import json2bulksql
from argo_bak.Global import argo_db
from argo_bak.Query import Query
from argo_bak.Settings import ARGO_FILENAME, PSQL_USER, RESULTS_FILENAME
from argo_bak.JSON2DB.argo import demo_init
import json

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    with open(ARGO_FILENAME, 'rb') as infile:
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
        return argo_db.execute_sql("SELECT * FROM argo_people_data;")


class DropCollectionArgo(Query):
    def __init__(self):
        super().__init__("Dropping Data from Argo")

    def db_command(self):
        return argo_db.execute_sql("DELETE FROM argo_ppp_data;")


class InitialLoadArgo(Query):
    def __init__(self):
        super().__init__("Loading Initial Data into Argo")

    def db_command(self):
        print("Starting...")
        PrepFilesArgo(ARGO_FILENAME).execute()
        data_copy_cmd = "\copy argo_people_data(objid, keystr, valstr, valnum, valbool) FROM '{0}' WITH DELIMITER '|';".format(
            RESULTS_FILENAME)
        # data_copy_cmd = "INSERT INTO argo_people_data OBJECT {0}".format(
        #         recommended_strings)
        load_data = subprocess.Popen(["psql", "--password", "-U", PSQL_USER, "-d", "argo", "-c", data_copy_cmd],
                                     stdout=subprocess.PIPE)

        load_data.communicate()
        # bool_copy_cmd = "\COPY argo_people_data(objid, keystr, valbool) FROM '{0}' WITH DELIMITER '|';".format(
        #     RESULTS_FILENAME)
        # load_bool = subprocess.Popen(["psql","--password", "-U", PSQL_USER, "-d", "argo", "-c", bool_copy_cmd],
        #                              stdout=subprocess.PIPE)
        #
        # num_copy_cmd = "\COPY argo_people_data(objid, keystr, valnum) FROM '{0}' WITH DELIMITER '|';".format(
        #     RESULTS_FILENAME)
        # load_num = subprocess.Popen(["psql", "--password", "-U", PSQL_USER, "-d", "argo", "-c", num_copy_cmd],
        #                             stdout=subprocess.PIPE)
        #
        # str_copy_cmd = "\COPY argo_people_data(objid, keystr, valstr) FROM '{0}' WITH DELIMITER '|';".format(
        #     RESULTS_FILENAME)
        # load_str = subprocess.Popen(["psql","--password", "-U", PSQL_USER, "-d", "argo", "-c", str_copy_cmd],
        #                             stdout=subprocess.PIPE)
        #
        # load_bool.communicate()
        # load_num.communicate()
        # load_str.communicate()


def InsertData():

    db = demo_init.get_db()
    with open(ARGO_FILENAME, 'r')as f:
        json_text = json.load(f)
    pprint(json_text)
    json_text = json.dumps(json_text)
    pprint(json_text)
    sql_text = f'INSERT INTO argo_people_data OBJECT {{ {json_text } }};'
    print(sql_text)
    for item in db.execute_sql(sql_text):
        print(json.dumps(item))
    print("DONE")


def main():
    tb_name = 'argo_people_data'
    argo_loader = InitialLoadArgo()
    argo_loader.db_command()
    path = 'JSON2DB/test/test4/hard.csv'
    # InsertData()
    ans1 = Query1Argo()
    ans1.db_command()


if __name__ == '__main__':
    main()
