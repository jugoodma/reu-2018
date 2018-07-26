# comments about this file
# 

import csv
from ast import literal_eval
import json
import re

spatial = input("filename: ./")
template_file = "output-template.html"
output = "output-data.html"
audioset = "../../data/unbalanced_train_segments.csv"
ave = "../../data/ave-all.csv"

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

# create labels lookup from ave
labels = {}
with open(ave, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = '&', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for row in reader:
        labels[row[1]] = row[0]

# load data from csv
data = {}
with open(spatial, 'r', newline = '') as f:
    reader = csv.reader(f)
    header = next(reader)
    count = -1
    for row in reader:
        y = row[0]
        l = labels[y]
        sec = row[1:]
        # some videos do not have all 10 seconds
        for i in range(int(len(sec) / 4)):
            count += 1
            r = []
            box = [literal_eval(sec[i * 4]), literal_eval(sec[i * 4 + 3])] # [(left, top), (right, bottom)]
            for idx in range(18):
                for jdx in range(32):
                    pos = (idx * 20 + 1, jdx * 20 + 1)
                    if box[0][0] <= pos[0] and pos[0] <= box[1][0] and box[0][1] <= pos[1] and pos[1] <= box[1][1]:
                        r.append(1)
                    else:
                        r.append(0)
            if data.get(y) is None:
                data[y] = []
            # ytid -> {file, ytid, label, response, start}
            data[y].append({"file": y + "-" + str(i) + "-" + str(i + 1) + ".jpg",
                            "ytid": y,
                            "label": l,
                            "response": r,
                            "assignment": "assignment-" + str(count),
                            "start": lookup[y] + i})

# sort each value based on start time
def k(obj):
    return obj['start']
for key in data:
    data[key].sort(key = k)

# replace json
template = open(template_file, 'r').read()
template = re.sub("\$\{data\}", json.dumps(data), template)
open(output, 'w').write(template)
