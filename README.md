Query Hybrid Provenance in OpenRefine
======================

Li, L., Ludäscher, B., & Zhang, Q. (2019). Towards more transparent, reproducible, and reusable data cleaning with OpenRefine. iConference 2019 Proceedings.

[Towards More Transparent, Reproducible, andReusable Data Cleaning with OpenRefine](http://hdl.handle.net/2142/103330)


[A first-principles algebraic approach to data transformations in data cleaning: understanding provenance from the ground up](	https://www.usenix.org/conference/tapp2020/presentation/nunez-corrales)


Overview
=========

For current Provenance model in OpenRefine, including operation history in `GUI`, `data.txt` file which includes more "complete" operation history, `history folder` which covers provenance information at cell level,all of three parts are incomplete, hard to reproduce and not transparent. 

To solve this, we propose to merge the provenance in archieve folder by pairing the history to data, in which the history id is provided to link them. We call this prov as Hybrid provenance. It gives the prospective provenance information from data.txt, such as what's the expression/computation method used in this operation; as well as the retrospective prov from history folders, such as what's the old value of this single cell, and what's the new value. 

As the data archived type in `data.txt` and `history folder` are not the same, the former uses JSON format; while the latter uses text/string. To make it more human & machine readable; quick to query, the [Repo](https://github.com/LanLi2017/parse_orhistory) has covered ten more prov rewritten, transposing the histroy into JSON format. 

### Generate Hybrid Prov

The command to generate hybrid provenance command line options is simple. 
Go into Project directory, edit the `run.bash` or use the command below:

    $ python hybrid.py --root_path [OpenRefine Archived folder] --log [Output hybrid prov folder name]


The last task is to do query with the hybrid provenance.
### 1. Hand-made Query Function  
Query directory has covered eight queries, such as reverse the data cleaning and get the clean dataset, return the operations applied on the single cell...

Query Description                                                 | Query command |
------------------------------------------------------------------|-----------
List all of changes applied on cell                               | changes-single-cell |
List all of operations applied on cell                            | operations-single-cell |
Count how many changes applied on cell                            | count-changes-single-cell |
Count how many operations aplied on cell                          |  count-operation-single-cell |
Reverse the data cleaning task and return the original cell value |  reverse-data |
List all of the cells which get changed                           | list-changed-cells |
Count how many cells have been changed                            | count-changed-cells |
Provenance of this single cell                                    | prov-single-cell |
return the whole query table                                      | merge |

You may now run the query using the above options simply by typing:

    $ python request.py --row [row index] --column [column index] --log [Hybrid prov file] --command [merge, default]


### 2. MongoDB query JSON

Use MongoDB to query Hybrid Prov. 


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
Query/dependency.py            | According to data transformatons in OpenRefine, return the dependencies       | 
Query/Options.py               | Arguments when run the query     |
Query/run.bash                 | Query runnable bash file      |
Query/result{\d}               | Query results       | 
data                           | Result of the reserved data cleaning query, return the clean dataset |
mongoDB                        | Using NoSQL to query Hybrid Prov       | 
mongoDB/createDB.py            | Create DB, collection, Insert Data |
mongoDB/input.json             | test JSON       | 
mongoDB.querys                 | test query with pymongo      |
\d+.project and \w+.project    | OpenRefine archived folder      |
log{\d}                        | store all of the hybrid prov      |
argo_bak                       | Argo/SQL, parse JSON into DBMS schema and do queries |




