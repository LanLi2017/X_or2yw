import glob
import json
import os
import re
import sqlite3
from pprint import pprint


def guess_data_type():
    pass


def merge_data(file_path):
    # read all the JSON files and
    infiles = sorted(glob.glob(os.path.join(file_path, '*.json')), key=os.path.getmtime)
    # filenames: data
    # filenames = []
    merge_data = []
    for infile in infiles:
        # find
        # filep = os.path.splitext(infile)[0]
        # filename = filep.split('/')[-1]
        # filenames.append(filename)
        with open(infile) as f:
            data = json.load(f)
        merge_data.append(data)
    # datas = list(zip(filenames, merge_data))
    return merge_data


# transformation
def extract_operation(hybrid_js):
    '''

    :param oh_json: hybrid json
    :return:
    '''
    column_name = []
    history_id = hybrid_js['id']
    try:
        pro_prov = hybrid_js['operation']
        table_name = pro_prov['op']
        for key, value in pro_prov.items():
            column_name.append(key)

    except:
        table_name = 'singleedit'

    return table_name, history_id, column_name


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insert_transformation_tb(hybrid_js, sql_f):
    """
    automatically insert values from JSON

    :param sql_f: sql file recording
    :param hybrid_js: hybrid Provenance json
    :return:
    """
    # automatically insert values from JSON
    # history_id ; step_index ; values
    for i, v in enumerate(hybrid_js):
        step_th = i
        history_id = v['id']
        try:
            op = v['operation']
            tb_name = op['op'].replace('/', '').replace('-', '')
            k_v = {
                k: f"{v}"
                for k, v in op.items()
                if k != 'edits'
            }
            sql_insert_transform = f'''INSERT INTO {tb_name}(history_id, step_index,{', '.join(k_v.keys())})VALUES ({history_id},{step_th},{', '.join(map(repr, k_v.values()))});'''

            sql_f.write(sql_insert_transform + '\n')
            # sql_f.write(f'''drop table if exists {tb_name};''')

        except:
            tb_name = 'singleedit'
            sql_insert_singleedit = f''' INSERT INTO {tb_name}(history_id, step_index,op)
                              VALUES({history_id},{step_th},"single_edit"); '''
            sql_f.write(sql_insert_singleedit + '\n')
            # sql_f.write(f'''drop table if exists {tb_name};''')


def insert_change_tb(hybrid_js, sql_f):
    '''
    history_id; row_id; column_id; new_value; old_value
    :return:
    '''
    # changes are saved in tuple key
    # pattern = re.compile('\(\d,\d\)')
    pattern = re.compile(r'\d+,\s*\d+')
    for i, v in enumerate(hybrid_js):
        history_id = v['id']
        for key, value in v.items():
            # if pattern.match(key):
            #     pass
            if isinstance(value, dict) and 'old' in value and 'new' in value:
                try:
                    row_id = value['row']
                    col_id = value['cell']
                except KeyError:
                    row_col = pattern.search(key).group().split(',')
                    row_id = int(row_col[0])
                    col_id = int(row_col[1])
                old = value['old']
                new = value['new']
                if old is not None and not isinstance(old, dict):
                    old_v = json.loads(old)['v']
                elif old is not None and isinstance(old, dict):
                    old_v = old['v']
                elif old is None:
                    old_v = old

                if new is not None and not isinstance(new, dict):
                    new_v = json.loads(new)['v']
                elif new is not None and isinstance(new, dict):
                    new_v = new['v']
                elif new is None:
                    new_v = new

                sql_insert_change = f''' INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES({history_id},{row_id},{col_id},"{new_v}","{old_v}"); '''
                sql_f.write(sql_insert_change + '\n')




def main():
    file_p = 'archive_logs/log/'
    DB = r"DataCleaning_wf.db"
    sql_f = open('workflow.sql', 'w')
    hybrid_prov = merge_data(file_p)

    # create dependency table
    # history_id: primary key
    # step_index: date cleaning step index
    # column_input: input column names;
    # column_output: output column names;
    # if diff(column_input, column_output) is null, no structure changes/ row-level/ single-edit
    sql_create_dependency_table = """ CREATE TABLE IF NOT EXISTS dependency(
                                          history_id integer primary key ,
                                          step_index integer NOT NULL ,
                                          column_input text,
                                          column_output text
    ); """
    sql_f.write(sql_create_dependency_table)
    # create change table
    # history id: primary key
    # row: row index
    # column: column index
    # new_value: new values after changes
    # old_value: old values before changes
    sql_create_change_table = """ CREATE TABLE IF NOT EXISTS change(
                                    history_id integer NOT NULL ,
                                    row_id integer NOT NULL ,
                                    column_id integer NOT NULL ,
                                    new_value text,
                                    old_value text,
                                    PRIMARY KEY (history_id, row_id, column_id),
                                    FOREIGN KEY (history_id) REFERENCES dependency (history_id)
    );

    """
    sql_f.write(sql_create_change_table)

    # create transformation tables
    sql_create_transformation_tables = []
    map_step_history = []
    transformation_name_list = []
    for i, value in enumerate(hybrid_prov):
        step_id = i
        table_name, history_id, column_name = extract_operation(value)
        map_step_history.append((step_id, history_id))

        sql_sens = ''
        for col in column_name:
            if col == 'edits':
                pass
            else:
                sql_sen = f'{col} text,'
                sql_sens += sql_sen
        if table_name not in transformation_name_list:
            tb_name = table_name.replace('/', '').replace('-', '')
            sql_create_transformation_tables.append(f"""CREATE TABLE IF NOT EXISTS {tb_name}(
                          history_id integer primary key,
                          step_index integer,
                          {sql_sens}
                          FOREIGN KEY (history_id) REFERENCES dependency (history_id)
            );""")

            transformation_name_list.append(table_name)
    for sql_create_transformation_table in sql_create_transformation_tables:
        sql_f.write(sql_create_transformation_table)

    insert_transformation_tb(hybrid_prov, sql_f)
    insert_change_tb(hybrid_prov, sql_f)

    sql_f.close()
    # create a database connection
    conn = create_connection(DB)
    #
    # # create tables:
    if conn is not None:
        # create dependency tables
        create_table(conn, sql_create_dependency_table)

        # create change tables
        create_table(conn, sql_create_change_table)

        # create all the transformation tables
        for transformation_table in sql_create_transformation_tables:
            create_table(conn, transformation_table)


if __name__ == '__main__':
    main()
