Query Hybrid Provenance in OpenRefine
======================


The yw-prototypes repository contains early implementations of YesWorkflow, an approach to modeling conventional scripts and programs as scientific workflows.  The software is described in these two publications:

* T. McPhillips, T. Song, T. Kolisnik, S. Aulenbach, K. Belhajjame, R.K. Bocinsky, Y. Cao, J. Cheney, F. Chirigati, S. Dey, J. Freire, C. Jones, J. Hanken, K.W. Kintigh, T.A. Kohler, D. Koop, J.A. Macklin, P. Missier, M. Schildhauer, C. Schwalm, Y. Wei, M. Bieda, B. Ludäscher (2015). **[YesWorkflow: A User-Oriented, Language-Independent Tool for Recovering Workflow Information from Scripts](http://ijdc.net/index.php/ijdc/article/view/10.1.298)**. *International Journal of Digital Curation* **10**, 298-313. [[PDF](http://ijdc.net/index.php/ijdc/article/download/10.1.298/401)]

* T. McPhillips, S. Bowers, K. Belhajjame, B. Ludäscher (2015). **[Retrospective Provenance Without a Runtime Provenance Recorder](https://www.usenix.org/conference/tapp15/workshop-program/presentation/mcphillips)**. *7th USENIX Workshop on the Theory and Practice of Provenance (TaPP'15)*. [[PDF](https://www.usenix.org/system/files/tapp15-mcphillips.pdf)]


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
