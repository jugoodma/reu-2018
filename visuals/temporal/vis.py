# comments about this file
# 

import csv
import json
import re

temporal = input("filename: ./")
template_file = "vis-template.html"
output = "vis-data.html"

# load data from csv
data = {}
with open(temporal, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    header = next(reader)
    for row in reader:
        if row[16] == 'Approved':
            r = []
            w = row[15]
            for i in range(40):
                r.append(int(row[i + 38]))
            if data.get(w) is None:
                data[w] = []
            data[w].append({"ytid": row[27],
                            "label": row[30],
                            "worker": w,
                            "assignment": row[14],
                            "response": r,
                            "start": int(row[28]),
                            "end": int(row[29]),
                            "contains": int(row[35]),
                            "hit": row[0]})

# sort each value based on the worker then the file
def k(obj):
    return obj['worker'], obj['ytid']
for key in data:
    data[key].sort(key = k)

# replace json
template = open(template_file, 'r').read()
template = re.sub("\$\{data\}", json.dumps(data), template)
open(output, 'w').write(template)
