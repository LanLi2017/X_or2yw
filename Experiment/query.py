# how many transformations change the cell at row 1, column 1
q1 = '''SELECT COUNT(history_id)
FROM change
WHERE row_id=1 and column_id=1;'''

# What are the new columns generated by column-split?
q2 = '''select column_output
'''

# What are the new columns generated by column-addition?
q = '''select history_id from transformation where op = "corecolumnaddition" '''

# What is the provenance of cell at row 1, column 4 ?


# what is the history of cell at row 1, column 4?
q3 = '''select '''

# select all the cells operated by Text-transform


# what's the original value of cell at row 0, column 0?


