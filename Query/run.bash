#python request.py --row 1 --column 2 --log log --command operations
#python request.py --row 1 --column 2 --log log --command changes
#python request.py --row 0 --column 0 --log log --command operations
#python request.py --log log --command most-value-changes
#python request.py --row 1 --column 2 --log log1 --command operations --out result1
#python request.py --row 1 --column 3 --log log1 --command operations --out result1

python request.py --row 1 --column 30 --log log2 --command operations --out result2
python request.py --row 1 --column 30 --log log2 --command changes --out result2
python request.py --log log2 --command most-value-changes --out result2
python request.py --row 1 --column 30 --log log2 --command count-changes --out result2
python request.py --row 1 --column 30 --log log2 --command count-operation --out result2
