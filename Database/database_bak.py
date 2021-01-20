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


def capture_merge_name(operation):
    exp = operation['expression']
    res = operation['baseColumnName']
    if exp == 'grel:value':
        #      missing information here: if no merge other columns, we still do not know if the new column is set
        # --------dependency as basecolumnName
        result = res
        # print('value: {}'.format(result))
        return [result]
    result = re.findall('\.\w+\.', exp)
    if result:
        newm = []
        for col in result:
            newm.append(col[1:len(col) - 1])
        result = newm
        return result
    else:
        result = re.findall('[A-Z]\w+ \d', exp)
        newm = []
        for col in result:
            newm.append(col)
        result = newm
        return result


def dep_tb(v):
    """
    automatically capture dependency relationship

    history_id; step index; column input; column output
    :return:column_input, output
    """

    opname = v['op']

    if opname == 'ColumnRenameChange':
        column_input = v['oldColumnName']
        column_output = v['newColumnName']
    elif opname == 'MassRowColumnChange':
        # TODO
        newColumnModel = v['newColumnModel']
        newcolumnnames = []
        oldcolumnnames = []
        for v in newColumnModel:
            newcolumns = json.loads(v)
            newcolumnnames.append(newcolumns['name'])
        oldColumnModel = v['oldColumnModel']
        for value in oldColumnModel:
            oldcolumns = json.loads(value)
            oldcolumnnames.append(oldcolumns['name'])
        column_input = ','.join(oldcolumnnames)
        column_output = ','.join(newcolumnnames)
    elif opname == 'ColumnAdditionChange':
        # TODO
        column_output = v['columnName']
        res = capture_merge_name(v['operation'])
        column_input = ','.join(res)
    else:
        if 'operation' in v:
            operation = v['operation']
            if 'columnName' in operation:
                # some operations change the structure only/ content only/ mixed
                if opname == 'MassCellChange':
                    column_input = v['commonColumnName']
                    column_output = column_input
                elif opname == 'ColumnRemovalChange':
                    column_output = None
                    column_input = operation['columnName']
                elif opname == 'ColumnSplitChange':
                    column_input = v['columnName']
                    column_output = ','.join(v['NewColumnNames'])
                else:
                    # TODO
                    column_input = operation['columnName']
                    column_output = column_input
            else:
                # row-level ops
                if opname == 'RowReorderChange':
                    # "sorting":
                    # {"criteria":
                    # [{"valueType":"number",
                    # "column":"id","blankPosition":2,"errorPosition":1,"reverse":false}]
                    sorting = operation['sorting']
                    column_input = sorting['criteria'][0]['column']
                    column_output = column_input
                else:
                    column_input = None
                    column_output = None

        else:
            # Specific op
            if opname == 'CellChange':
                desc = v['description']  # "Edit single cell on row 6196, column year"
                col_index = desc.split(' ').index('column')
                column_name = desc.split(' ')[col_index + 1]
                column_input = column_name
                column_output = column_input
            else:
                column_input = None
                column_output = None

    return column_input, column_output


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
            sql_insert_transform = f'''INSERT INTO {tb_name}(history_id,{', '.join(k_v.keys())})VALUES ({history_id},{', '.join(map(repr, k_v.values()))});'''

            sql_f.write(sql_insert_transform + '\n')
            # sql_f.write(f'''drop table if exists {tb_name};''')

        except:
            tb_name = 'singleedit'
            sql_insert_singleedit = f''' INSERT INTO {tb_name}(history_id, op)
                              VALUES({history_id},"singleedit"); '''
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
                    old_v = ''

                if new is not None and not isinstance(new, dict):
                    new_v = json.loads(new)['v']
                elif new is not None and isinstance(new, dict):
                    new_v = new['v']
                elif new is None:
                    new_v = ''

                sql_insert_change = f''' INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES({history_id},{row_id},{col_id},"{new_v}","{old_v}"); '''
                sql_f.write(sql_insert_change + '\n')


def main():
    file_p = 'archive_logs/log/'
    DB = r"DataCleaning_wf.db"
    sql_f = open('workflow.sql', 'w')
    sql_f.write(f'''drop table if exists change;''' + '\n')
    sql_f.write(f'''drop table if exists transformation;''' + '\n')
    sql_f.write(f'''drop table if exists dependency;''' + '\n')
    sql_f.write(f'''drop table if exists transformation_params;''' + '\n')
    hybrid_prov = merge_data(file_p)

    # create change table
    # history id: primary key
    # row: row index
    # column: column index
    # new_value: new values after changes
    # old_value: old values before changes
    sql_create_change_table = """ CREATE TABLE IF NOT EXISTS change(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        history_id integer NOT NULL ,
                                        row_id integer NOT NULL ,
                                        column_id integer NOT NULL ,
                                        new_value text,
                                        old_value text,
                                        UNIQUE (history_id, row_id, column_id),
                                        FOREIGN KEY (history_id) REFERENCES transformation (history_id)
        );

        """
    sql_f.write(sql_create_change_table)

    # create transformation list tables: map to transformations
    sql_create_trans_list_table = """CREATE TABLE IF NOT EXISTS transformation(
                                            history_id integer PRIMARY KEY ,
                                            step_index integer NOT NULL ,
                                            op text,
                                            column_input text,
                                            column_output text

        );

        """
    sql_f.write(sql_create_trans_list_table)
    # create transformation tables with op names
    sql_create_transformation_tables = []
    map_step_history = []
    transformation_name_list = []
    for i, value in enumerate(hybrid_prov):
        step_id = i
        table_name, history_id, column_name = extract_operation(value)
        tb_name = table_name.replace('/', '').replace('-', '')
        column_input, column_output = dep_tb(value)
        map_step_history.append((step_id, history_id))

        sql_sens = ''
        for col in column_name:
            if col == 'edits':
                pass
            else:
                sql_sen = f'{col} text,'
                sql_sens += sql_sen

        if table_name not in transformation_name_list:
            sql_create_transformation_tables.append(f"""CREATE TABLE IF NOT EXISTS {tb_name}(
                          history_id integer primary key,
                          {sql_sens}
                          FOREIGN KEY (history_id) REFERENCES transformation (history_id)
            );""")

            transformation_name_list.append(table_name)
        sql_insert_transformations = f''' INSERT INTO transformation(history_id, step_index,op,column_input, column_output) VALUES({history_id},{step_id},"{tb_name}","{column_input}", "{column_output}");'''
        sql_f.write(sql_insert_transformations + '\n')
    for sql_create_transformation_table in sql_create_transformation_tables:
        sql_f.write(sql_create_transformation_table)

    insert_transformation_tb(hybrid_prov, sql_f)
    insert_change_tb(hybrid_prov, sql_f)


    sql_f.close()


if __name__ == '__main__':
    main()
