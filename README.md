Query Hybrid Provenance in OpenRefine
======================




Architect
---------
Directory                      | Content Description |
-------------------------------|-------------------------------------------------------------------------------------------|
parse_orhistory                | [Repo](https://github.com/LanLi2017/parse_orhistory) helps reconstruct prov into JSON     |
hybrid.py                      | hybrid prov, by merging/pairing operation history from data folder with history folder    | 
Options.py                     | command generating hybrid provenance                                                      | 
run.bash                       | run and generate hybrid prov into log* folder                                             | 
Query                          | hand-made Query Function                                                                  |
Query/request.py               | All of the query functions                                                                | 
Query/dependency.py            | .R       | 
Query/Options.py               | .R       |
Query/run.bash                 | .R       |
Query/result{\d}               | Query results       | 
mongoDB                        | Using NoSQL to query Hybrid Prov       | 
mongoDB/createDB.py            | Create DB, collection, Insert Data |
mongoDB/input.json             | test JSON       | 
mongoDB.querys                 | test query with pymongo      |
\d+.project and \w+.project    | OpenRefine archived folder      |
log{\d}                        | store all of the hybrid prov      |
argo_bak                       | Argo/SQL, parse JSON into DBMS schema and do queries |



Overview
--------


# X_or2yw
Extended or2yw toolkit 

Hybrid JSON file:
Pairling combined provenance file from history folder and data.txt

Query and Answer:

Encapsulated 10* queries; 
run bash and output the result


JSON to DB schema:
Under construction
