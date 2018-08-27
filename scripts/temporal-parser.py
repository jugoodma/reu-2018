import os
import csv
from settings import *

data = []

for filename in os.listdir(result_path + "temporal/contains"):
    with open(result_path + "temporal/contains/" + filename, 'r', newline = '') as f:
        reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL)
        h = next(reader)
        for row in reader:
            # do not include 
            if not row[20] == "":
                sec = []
                for i in range(40):
                    sec.append(row[i + 38])
                data.append({"ytid": row[27], "label": row[30], "sec": sec, "time": int(row[29]) - int(row[28])})

with open(result_path + "ave-expand.csv", 'w', newline = '') as f:
    writer = csv.writer(f, delimiter = '&', quotechar = '"')
    for obj in data:
        print(obj)
        s = []
        for i in range(obj['time']):
            stemp = 0
            for j in range(4):
                stemp += int(obj['sec'][4 * i + j])
            if stemp > 0:
                s.append(1)
            else:
                s.append(0)
        start = -1
        for i in range(obj['time']):
            if s[i] == 1 and start == -1:
                start = i
        end = -1
        for i in range(obj['time']):
            if s[obj['time'] - 1 - i] == 1 and end == -1:
                end = obj['time'] - i
        print(str(s) + ", " + str(start) + ", " + str(end))
        writer.writerow([obj['label'], s, obj['ytid']])
