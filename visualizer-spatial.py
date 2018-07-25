import csv
import re
import json
from settings import *

input_data = input("spatial file name: ./results/")
output_path = 'visuals/'

template = open(template_path + 'spatial-visualizer-ui.html', 'r').read()
prog = re.compile("^Answer\.loc\-(\d\d\d)$")

with open(result_path + input_data, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    """
    # if we were good programmers we'd calculate where the locations of everything are, but i'm lazy
    loc_arr = [] # contains index positions of each Answer.loc-###
    loc_reg = [] # contains the actual number location from the above index
    input_arr = [] # [Input.ytid, Input.start, Input.end, Input.label]
    input_reg = [] # contains the regex for the above positions
    hitid = 0 # hitid index
    for idx, ele in enumerate(next(reader)):
        m = prog.match(ele)
        if m:
            loc_arr.append(idx)
            loc_reg.append(int(m.group(1)))
        else if ele == "Input.ytid":
            input_arr.append(idx)
            input_reg.append("\$\{ytid\}")
        else if ele == "Input.start":
            input_arr.append(idx)
            input_reg.append("\$\{start\}")
        else if ele == "Input.end":
            input_arr.append(idx)
            input_reg.append("\$\{end\}")
        else if ele == "Input.label":
            input_arr.append(idx)
            input_reg.append("\$\{label\}")
        else if ele == "HITId":
            hitid = idx
    for row in reader:
        out = open(output_path + 'spatial-hit-' + row[hitid] + '.html', 'w')
        temp = template
        for i in range(4): # hard coded length
            temp = re.sub(input_reg[i], row[input_arr[i]], temp)
        darr = {}
        for i in range(576): # hard coded length
            darr[]
        temp = re.sub('', '<input type="hidden" ' + row[loc_arr[i]] + ' />', temp)
    """
    next(reader)
    for row in reader:
        out = open(output_path + 'spatial-hit-' + row[0] + '.html', 'w')
        temp = template
        temp = re.sub("\$\{ytid\}", row[27], temp)
        temp = re.sub("\$\{start\}", row[28], temp)
        temp = re.sub("\$\{end\}", row[29], temp)
        temp = re.sub("\$\{label\}", row[30], temp)
        darr = []
        for i in range(576):
            darr.append(row[i + 36])
        temp = re.sub("\$\{dankmemes\}", json.dumps(darr), temp)
        out.write(temp)
