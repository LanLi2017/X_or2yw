drop table if exists change;
drop table if exists transformation;
drop table if exists dependency;
drop table if exists transformation_params;
 CREATE TABLE IF NOT EXISTS change(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        history_id integer NOT NULL ,
                                        row_id integer NOT NULL ,
                                        column_id integer NOT NULL ,
                                        new_value text,
                                        old_value text,
                                        UNIQUE (history_id, row_id, column_id),
                                        FOREIGN KEY (history_id) REFERENCES transformation (history_id)
        );

        CREATE TABLE IF NOT EXISTS transformation(
                                            history_id integer PRIMARY KEY ,
                                            step_index integer NOT NULL ,
                                            op text,
                                            column_input text,
                                            column_output text

        );

         INSERT INTO transformation(history_id, step_index,op,column_input, column_output) VALUES(1591902529907,0,"coretexttransform","Login email", "Login email");
 INSERT INTO transformation(history_id, step_index,op,column_input, column_output) VALUES(1591902621963,1,"coretexttransform","Identifier", "Identifier");
 INSERT INTO transformation(history_id, step_index,op,column_input, column_output) VALUES(1591902583373,2,"coretexttransform","First name", "First name");
 INSERT INTO transformation(history_id, step_index,op,column_input, column_output) VALUES(1591902689351,3,"coretexttransform","Last name", "Last name");
 INSERT INTO transformation(history_id, step_index,op,column_input, column_output) VALUES(1591902466488,4,"corecolumnaddition","", "group");
CREATE TABLE IF NOT EXISTS coretexttransform(
                          history_id integer primary key,
                          op text,description text,engineConfig text,columnName text,expression text,onError text,repeat text,repeatCount text,
                          FOREIGN KEY (history_id) REFERENCES transformation (history_id)
            );CREATE TABLE IF NOT EXISTS corecolumnaddition(
                          history_id integer primary key,
                          op text,description text,engineConfig text,newColumnName text,columnInsertIndex text,baseColumnName text,expression text,onError text,
                          FOREIGN KEY (history_id) REFERENCES transformation (history_id)
            );INSERT INTO coretexttransform(history_id,op, description, engineConfig, columnName, expression, onError, repeat, repeatCount)VALUES (1591902529907,'core/text-transform', "Text transform on cells in column Login email using expression grel:value.split('@')[0]", "{'facets': [], 'mode': 'row-based'}", 'Login email', "grel:value.split('@')[0]", 'keep-original', 'False', '10');
INSERT INTO coretexttransform(history_id,op, description, engineConfig, columnName, expression, onError, repeat, repeatCount)VALUES (1591902621963,'core/text-transform', 'Text transform on cells in column Identifier using expression value.toNumber()', "{'facets': [], 'mode': 'row-based'}", 'Identifier', 'value.toNumber()', 'keep-original', 'False', '10');
INSERT INTO coretexttransform(history_id,op, description, engineConfig, columnName, expression, onError, repeat, repeatCount)VALUES (1591902583373,'core/text-transform', 'Text transform on cells in column First name using expression value.toUppercase()', "{'facets': [], 'mode': 'row-based'}", 'First name', 'value.toUppercase()', 'keep-original', 'False', '10');
INSERT INTO coretexttransform(history_id,op, description, engineConfig, columnName, expression, onError, repeat, repeatCount)VALUES (1591902689351,'core/text-transform', 'Text transform on cells in column Last name using expression value.toUppercase()', "{'facets': [], 'mode': 'row-based'}", 'Last name', 'value.toUppercase()', 'keep-original', 'False', '10');
INSERT INTO corecolumnaddition(history_id,op, description, engineConfig, newColumnName, columnInsertIndex, baseColumnName, expression, onError)VALUES (1591902466488,'core/column-addition', "Create column group at index 2 based on column Identifier using expression grel:if(value>5000,'admin','user')", "{'facets': [], 'mode': 'row-based'}", 'group', '2', 'Identifier', "grel:if(value>5000,'admin','user')", 'set-to-blank');
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902529907,0,0,"laura","laura@example.com"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902529907,1,0,"craig","craig@example.com"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902529907,2,0,"mary","mary@example.com"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902529907,3,0,"jamie","jamie@example.com"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902621963,0,1,"2070"," 2070"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902621963,1,1,"4081"," 4081"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902621963,2,1,"9346"," 9346"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902621963,3,1,"5079"," 5079"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902583373,0,2," LAURA"," Laura"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902583373,1,2," CRAIG"," Craig"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902583373,2,2," MARY"," Mary"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902583373,3,2," JAMIE"," Jamie"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902689351,0,3," GREY"," Grey"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902689351,1,3," JOHNSON"," Johnson"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902689351,2,3," JENKINS"," Jenkins"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902689351,3,3," SMITH"," Smith"); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902466488,0,4,"user",""); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902466488,1,4,"user",""); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902466488,2,4,"admin",""); 
 INSERT INTO change (history_id, row_id,column_id,new_value, old_value)VALUES(1591902466488,3,4,"admin",""); 
