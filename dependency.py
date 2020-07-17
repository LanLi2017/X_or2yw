import re
from pprint import pprint


class OPDependency:
    # return dependency: Geometric Transformations: change the structure of datasets, not only their content.
    # operation which could change the identifier (row/column)
    # Cell --> column name --> prepend (n-1) provenance on this column
    def __init__(self,data):
        # dependency: previous dep + follow dep
        # previous: add columns:  1.basecolumn 2. expression ;
        # future: add columns: ;
        # delete columns: -->
        # transpose: add + delete

        # previous column dependency
        self.prev_dep = []
        # future column dependency; e.g. split column will generate new columns
        # suffix column dependency:
        self.suf_dep = []
        self.data = data
        self.operation = self.data['operation']
        if self.operation['op']:
            self.opname = self.operation['op']
        else:
            self.opname = 'single-edit'

    def mapping(self):
        '''
         "column-addition": opd.add_column,
        "column-split": opd.split_column,
        "column-rename": opd.rename_column,
        "column-removal": opd.remove_column
        '''
        # op_name = self.mapping_ops_name[self.history_id]

        if self.opname == 'column-addition':
            return self.add_column_d()
        elif self.opname == 'column-split':
            return self.split_column_d()
        elif self.opname== 'column-rename':
            return self.rename_column_d()
        elif self.opname == 'column-removal':
            return self.remove_column_d()
        elif self.opname == 'text-transform':
            return self.text_transform_d()
        elif self.opname == 'core/row-reorder':
            return self.row_reorder()
        elif self.opname == 'core/transpose-columns-into-rows':
            return self.transpose()
        elif self.opname == 'core/row-removal':
            return self.remove_row()
        elif self.opname == 'core/column-move':
            return self.column_move()

    def add_column_d(self):
        '''
        {'baseColumnName': 'Mode',
          'columnInsertIndex': 4,
          'description': 'Create column Mode_font at index 4 based on column Mode '
                         'using expression grel:cells.Mode.value + '
                         'cells.Font_size.value',
          'engineConfig': {'facets': [], 'mode': 'row-based'},
          'expression': 'grel:cells.Mode.value + cells.Font_size.value',
          # 'cells['Mode'].value + cells['Font_size'].value'
          # "expression": "grel:if(cells.id.value > 3, \"big string\", \"small string\")",
          'newColumnName': 'Mode_font',
          'onError': 'set-to-blank',
          'op': 'core/column-addition'}
        '''
        # add column expressions:
        # cells["Column 1"].value + cells["Column 2"].value
        # cells.MyCol1.value + cells.MyCol2.value
        # row.record.cells.AuthorFirstName.value + " " + row.record.cells.AuthorLastName.value
        newcolumn = self.operation['newColumnName']
        self.suf_dep.append(newcolumn)

        baseColumnName = self.operation['baseColumnName']
        expression = self.operation['expression']
        exp = expression.lstrip('grel:')
        # UA: how to parse GREL?
        if re.findall(r"cells\.(.+?)\.", exp):
            pattern = re.findall(r"cells\.(.+?)\.", exp)
            self.prev_dep.extend(pattern)
            # re.findall(r"cells\['(.+?)'\]", exp)
        elif re.findall(r"cells\['(.+?)'\]", exp):
            pattern = re.findall(r"cells\['(.+?)'\]", exp)
            self.prev_dep.extend(pattern)
        else:
            pass

        # try:
        #     # re.match(r'^\((\d+), (\d+)\)$', key)
        #     input_nodes = re.findall(r"^cells\.(.*)\.value$",expression)
        # else:
        #     print('here')
        # finally:
        #     print('ok')

    def split_column_d(self):
        '''
         'columnName': 'Author',
         'description': '...',
         'engineConfig': {'facets': [], 'mode': 'row-based'},
         'guessCellType': True,
         'maxColumns': 0,
         'mode': 'separator',
         'op': 'core/column-split',
         'regex': False,
         'removeOriginalColumn': True,
         'separator': '#'
        incompleteness not approve : except 'desciption'
        There is no record for new generated columns in OpenRefine
        '''
        columnName = self.operation['columnName']
        self.prev_dep.append(columnName)
        # NewColumnNames
        self.suf_dep.extend(self.data['NewColumnNames'])
        # split_d = (input_node, split_cols)

    def remove_column_d(self):
        '''
         {'columnName': 'Danmaku_pool',
          'description': 'Remove column Danmaku_pool',
          'op': 'core/column-removal'}]
        '''
        dep_col = self.operation['columnName']
        self.prev_dep.append(dep_col)

    def rename_column_d(self):
        '''
          'description': 'Rename column Showing_time to Video_Time',
          'newColumnName': 'Video_Time',
          'oldColumnName': 'Showing_time',
          'op': 'core/column-rename'},
        '''
        old_col = self.operation['oldColumnName']
        new_col = self.operation['newColumnName']
        self.prev_dep.append(old_col)
        self.suf_dep.append(new_col)
        # return (input, output)

    def text_transform_d(self):
        # rigid transformation
        '''
           "op": "core/text-transform",
            "description": "Text transform on cells in column Author using expression value.replace(\"#\",\" \")",
            "columnName": "Author",
            "expression": "value.replace(\"#\",\" \")",
        '''
        col = self.operation['columnName']
        self.prev_dep.append(col)

    def row_reorder(self):
        # reorder row, without changing the identifier
        '''
                    [
          {
            "op": "core/row-reorder",
            "mode": "record-based",
            "sorting": {
              "criteria": [
                {
                  "valueType": "number",
                  "column": "id",
                  "blankPosition": 2,
                  "errorPosition": 1,
                  "reverse": false
                }
              ]
            },
            "description": "Reorder rows"
          }
        ]
                    '''
        # dep_col = self.operation['sorting']['criteria'][0]['column']
        pass

    def transpose(self):
        # under construction
        '''
        [
          {
            "op": "core/transpose-columns-into-rows",
            # "combinedColumnName": "idx",
            "startColumnName": "id",
            "columnCount": -1,
            "ignoreBlankCells": true,
            "fillDown": false,
            "separator": null,
            "keyColumnName": "identifier",
            "valueColumnName": "value",
            "description": "Transpose cells in columns starting with id into rows in two new columns named identifier and value"
          }
        ]
        :return:
        '''
        keycolumn = self.operation['keyColumnName']
        valuecolumn = self.operation['valueColumnName']
        if self.operation['combinedColumnName']:
            self.suf_dep.append(self.operation['combinedColumnName'])
        else:
            self.suf_dep.append(keycolumn)
            self.suf_dep.append(valuecolumn)

    def remove_row(self):
        '''
        [
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "classify",
          "expression": "value",
          "columnName": "classify",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "big string",
                "l": "big string"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "description": "Remove rows"
  }
]
        :return:
        '''
        pass

    def column_move(self):
        '''{
            "op": "core/column-move",
            "columnName": "tag",
            "index": 1,
            "description": "Move column tag to position 1"
        }'''
        pass


def main():
    # test
    pass


if __name__ == '__main__':
    # test()
    main()