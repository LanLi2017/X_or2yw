# cell at row * column *, what's the function ?
# cell at row * column *, what're the changes?
# given row index, column index, return cell workflow
import glob
import json
import os

import Options


def getvalue(data:str):
    if isinstance(data, dict):
        return data['v']
    else:
        try:
            value = json.loads(data)
            return value['v']
        except TypeError:
            return None


def main():
    # args
    args = Options.get_args()
    row = args.row
    column = args.column

    # row = 2
    # column = 1

    path = f'../{args.log}/'
    # path ='../log/'
    infiles = sorted(glob.glob(os.path.join(path, '*.json')), key=os.path.getmtime)

    # ask what?
    return_command = args.command
    # return_command = 'changes'
    # return_command = 'operations'
    res = []
    for infile in infiles:
        # find
        filep = os.path.splitext(infile)[0]
        filename = filep.split('/')[-1]
        with open(infile) as f:
            data = json.load(f)
            for key, value in data.items():
                if key == str((row, column)):
                    # return choice: 1. operations 2. cell changes
                    if return_command == 'changes':
                        old_value = getvalue(value['old'])
                        olddict = {old_value: (row, column)}
                        new_value = getvalue(value['new'])
                        newdict = {new_value: (row, column)}
                        res.append((filename, olddict, newdict))
                    elif return_command == 'operations':
                        ops = data['operation']
                        # innerdicts = json.loads(ops)
                        res.append(ops['expression'])

    # output = f'result/{args.out}'
    log_folder = 'result/'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    output = f'result/{return_command}_row{args.row}_column{args.column}.txt'
    with open(output, 'w')as file:
        file.write(str(res))
    return res


if __name__ == '__main__':
    main()