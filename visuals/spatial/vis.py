# comments about this file
# 

import csv
import json
import re

spatial = input("filename: ./")
template_file = "vis-template.html"
output = "vis-data.html"
audioset = "../../data/unbalanced_train_segments.csv"
config = "config.json"

# create lookup for absolute to relative times
# ytid -> start time of actual youtube video
lookup = {}
with open(audioset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for i in range(3):
        next(reader)
    for row in reader:
        if lookup.get(row[0]) is None:
            lookup[row[0]] = int(float(row[1]))

# load data from csv
data = {}
with open(spatial, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    header = next(reader)
    for row in reader:
        w = row[15]
        y = row[27]
        s = int(row[28])
        r = []
        for i in range(576):
            r.append(int(row[i + 36]))
        if data.get(w) is None:
            data[w] = []
        data[w].append({"file": y + "-" + str(s) + "-" + str(s + 1) + ".jpg",
                        "ytid": y,
                        "label": row[30],
                        "worker": row[15],
                        "assignment": row[14],
                        "response": r,
                        "start": lookup[y] + s,
                        "hit": row[0]})

# sort each value based on the worker then the file
def k(obj):
    return obj['worker'], obj['file']
for key in data:
    data[key].sort(key = k)

# replace json
template = open(template_file, 'r').read()
template = re.sub("\$\{data\}", json.dumps(data), template)
template = re.sub("\$\{config\}", open(config, 'r').read(), template)
open(output, 'w').write(template)
