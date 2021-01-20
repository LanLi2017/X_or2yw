drop table if exists change;
drop table if exists transformation;
drop table if exists dependency;
drop table if exists transformation_params;
CREATE TABLE IF NOT EXISTS change
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id integer NOT NULL,
    row_id     integer NOT NULL,
    column_id  integer NOT NULL,
    new_value  text,
    old_value  text,
    UNIQUE (history_id, row_id, column_id),
    FOREIGN KEY (history_id) REFERENCES transformation (history_id)
);

CREATE TABLE IF NOT EXISTS transformation
(
    history_id    integer PRIMARY KEY,
    step_index    integer NOT NULL,
    op            text,
    column_input  text,
    column_output text

);

CREATE TABLE IF NOT EXISTS transformation_params
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id  integer,
    param_name  text,
    param_value text,
    FOREIGN KEY (history_id) REFERENCES transformation (history_id)
);
INSERT INTO transformation(history_id, step_index, op, column_input, column_output)
VALUES (1591902529907, 0, "coretexttransform", "Login email", "Login email");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "op", "core/text-transform");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "description",
        "Text transform on cells in column Login email using expression grel:value.split('@')[0]");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "engineConfig", "{'facets': [], 'mode': 'row-based'}");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "columnName", "Login email");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "expression", "grel:value.split('@')[0]");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "onError", "keep-original");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "repeat", "False");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902529907, "repeatCount", "10");
INSERT INTO transformation(history_id, step_index, op, column_input, column_output)
VALUES (1591902621963, 1, "coretexttransform", "Identifier", "Identifier");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "op", "core/text-transform");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "description", "Text transform on cells in column Identifier using expression value.toNumber()");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "engineConfig", "{'facets': [], 'mode': 'row-based'}");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "columnName", "Identifier");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "expression", "value.toNumber()");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "onError", "keep-original");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "repeat", "False");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902621963, "repeatCount", "10");
INSERT INTO transformation(history_id, step_index, op, column_input, column_output)
VALUES (1591902583373, 2, "coretexttransform", "First name", "First name");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "op", "core/text-transform");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "description",
        "Text transform on cells in column First name using expression value.toUppercase()");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "engineConfig", "{'facets': [], 'mode': 'row-based'}");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "columnName", "First name");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "expression", "value.toUppercase()");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "onError", "keep-original");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "repeat", "False");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902583373, "repeatCount", "10");
INSERT INTO transformation(history_id, step_index, op, column_input, column_output)
VALUES (1591902689351, 3, "coretexttransform", "Last name", "Last name");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "op", "core/text-transform");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "description",
        "Text transform on cells in column Last name using expression value.toUppercase()");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "engineConfig", "{'facets': [], 'mode': 'row-based'}");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "columnName", "Last name");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "expression", "value.toUppercase()");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "onError", "keep-original");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "repeat", "False");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902689351, "repeatCount", "10");
INSERT INTO transformation(history_id, step_index, op, column_input, column_output)
VALUES (1591902466488, 4, "corecolumnaddition", "", "group");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "op", "core/column-addition");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "description",
        "Create column group at index 2 based on column Identifier using expression grel:if(value>5000,'admin','user')");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "engineConfig", "{'facets': [], 'mode': 'row-based'}");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "newColumnName", "group");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "columnInsertIndex", "2");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "baseColumnName", "Identifier");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "expression", "grel:if(value>5000,'admin','user')");
INSERT INTO transformation_params(history_id, param_name, param_value)
VALUES (1591902466488, "onError", "set-to-blank");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902529907, 0, 0, "laura", "laura@example.com");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902529907, 1, 0, "craig", "craig@example.com");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902529907, 2, 0, "mary", "mary@example.com");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902529907, 3, 0, "jamie", "jamie@example.com");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902621963, 0, 1, "2070", " 2070");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902621963, 1, 1, "4081", " 4081");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902621963, 2, 1, "9346", " 9346");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902621963, 3, 1, "5079", " 5079");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902583373, 0, 2, " LAURA", " Laura");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902583373, 1, 2, " CRAIG", " Craig");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902583373, 2, 2, " MARY", " Mary");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902583373, 3, 2, " JAMIE", " Jamie");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902689351, 0, 3, " GREY", " Grey");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902689351, 1, 3, " JOHNSON", " Johnson");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902689351, 2, 3, " JENKINS", " Jenkins");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902689351, 3, 3, " SMITH", " Smith");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902466488, 0, 4, "user", "");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902466488, 1, 4, "user", "");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902466488, 2, 4, "admin", "");
INSERT INTO change (history_id, row_id, column_id, new_value, old_value)
VALUES (1591902466488, 3, 4, "admin", "");
