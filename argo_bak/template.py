# args: history path
# his_path = '1660451457167.project/history/'
# # args: extract folder path
# extract_p = 'extract_history/'
# if not os.path.exists(extract_p):
#     os.makedirs(extract_p)
#
# infiles = sorted(glob.glob(os.path.join(his_path, '*.change.zip')), key=os.path.getmtime)
# print(infiles)
#
# for infile in infiles:
#     unzip(infile, extract_p)


# import pandas as pd
# df = pd.read_csv('data/1660451457167_clean.csv')
# print(df.iat[0,1])
import re

prev_dep = []
# if re.match(r'grel:cells\.(.*)\.value\s\+\scells.(.*).value', expression):
#     pattern = re.match(r'grel:cells\.(.*)\.value\s\+\scells.(.*).value', expression)
#     prev_dep.append(pattern.group(1))
#     prev_dep.append(pattern.group(2))
#
# # print(prev_dep)
#
# prev_dep1 = []
# exp1 = "grel:cells['Mode'].value + cells['Font_size'].value"
# if re.match(r'grel:cells\[\'(.*)\'\]\.value\s\+\scells\[\'(.*)\'\]\.value', exp1):
#     pattern1 = re.match(r'grel:cells\[\'(.*)\'\]\.value\s\+\scells\[\'(.*)\'\]\.value', exp1)
#     prev_dep1.append(pattern1.group(1))
#     prev_dep1.append(pattern1.group(2))
# else:

#     print('404')

expression = 'grel:cells.Mode.value + cells.Font_size.value'
# expression = "grel:cells['Mode 1'].value + cells['Font_size 2'].value"
exp = expression.lstrip('grel:')
#  (r'cells[\'(.+)\']')
# r"cells\['(.+?)'\]"
res = re.findall(r"cells\.(.+?)\.", exp)
prev_dep.extend(res)
print(prev_dep)
# if re.match(r'',expression):
#     pattern = re.match(r'',expression)
#     prev_dep.append(pattern.group(1))
#     prev_dep.append(pattern.group(2))
#
# print(prev_dep)