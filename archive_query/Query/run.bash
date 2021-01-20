#python request.py --log log6 --row 2 --column 4 --out result4
#python request.py  --row 0 --column 0 --log log7 --command prov-single-cell --out result5 --data DTA_clean.csv
#python request.py --row 1 --column 1 --log log7 --command prov-single-cell --out result5 --data DTA_clean.csv
#python request.py --row 2 --column 4 --log log7 --command prov-single-cell --out result5 --data DTA_clean.csv
#python request.py --row 2 --column 4 --log log7 --command merge --out result5 --data DTA_clean.csv
python request.py --row 1 --column 3 --log log7 --command merge --out result5 --data DTA_clean.csv
#python request.py --row 1 --column 3 --log log7 --command reverse-data --out result5 --data DTA_clean.csv
python request.py --row 0 --column 1 --log log7 --command merge --out result5 --data DTA_clean.csv


#python request.py --row 1 --column 2 --log log --command operations
#python request.py --row 1 --column 2 --log log --command changes
#python request.py --row 0 --column 0 --log log --command operations
#python request.py --log log --command most-value-changes
#python request.py --row 1 --column 2 --log log1 --command operations --out result1
#python request.py --row 1 --column 3 --log log1 --command operations --out result1

#airbnb data
#python request.py --row 1 --column 30 --log log2 --command changes-single-cell --out result2
#python request.py --row 1 --column 30 --log log2 --command operations-single-cell --out result2
#python request.py --log log2 --command most-value-changes --out result2
#python request.py --row 1 --column 30 --log log2 --command count-changes-single-cell --out result2
#python request.py --row 1 --column 30 --log log2 --command count-operation-single-cell --out result2
#python request.py --log log2 --command list-changed-cells --out result2

# demo data
#python request.py --row 1 --column 2 --log log1 --command changes-single-cell --out result1
#python request.py --row 0 --column 0 --log log1 --command operations-single-cell --out result1
#python request.py --log log1 --command most-value-changes --out result1
#python request.py --row 1 --column 2 --log log1 --command count-changes-single-cell --out result1
#python request.py --row 1 --column 2 --log log1 --command count-operation-single-cell --out result1
#python request.py --log log1 --command list-changed-cells --out result1
#python request.py --row 0 --column 0 --log log1 --command changes-single-cell --out result1
#python request.py --row 0 --column 0 --log log1 --command reverse-data --out result1
#
#python request.py --log log1 --command most-value-changes --out result1
#python request.py --log log2 --command most-value-changes --out result1
#python request.py --log log3 --row 0 --column 0 --command changes-single-cell --out result3
#python request.py --log log3 --row 0 --column 0 --command operations-single-cell --out result3
#python request.py --log log3 --row 0 --column 0 --command  count-changes-single-cell --out result3
#python request.py --log log3 --row 0 --column 0 --command  count-operation-single-cell --out result3
#python request.py --log log4 --row 2 --column 4 --out result4
#python request.py --log log4 --row 2 --column 4 --command changes-single-cell --out result4