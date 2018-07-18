import csv
import numpy
import itertools
from settings import *

input_data = 'spatial-output.csv'

output_data = 'spatial-batch-output-parsed.csv'
temp_data = './data/tempt_data.csv'
#row[36] first location row[612] last location

reader = csv.reader(open(result_path + input_data, 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)

writer = csv.writer(open(data_path + output_data, 'w', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)

def prettyprint(arr):
    for i in range(18):
        row = ''
        for j in range(32):
            row += arr[(i * 32) + j] + ' '
        print(row)
    print("---------------------------------------------------------------")

def prettyprintoverlay(arr):
    for row in arr:
        print(' '.join([str(int(x)) for x in row]))
    print("---------------------------------------------------------------")

templist = []
templist.append('ytid')

for i in range(10):
    templist.append('second' + str(i+1))
    for i in range(3):
        templist.append('')

writer.writerow(templist)

f = open(temp_data, 'w', newline = '')

writer2 = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)


writer2.writerow(next(reader))

overlay_array = numpy.zeros((18, 32))

def compare(lst):
    return lst[27], lst[28]

output = []

for row in reader:
    if row[19] != "":
        output.append(row)

output.sort(key = compare)


output_hash = {}

for row in output:
    if row[27] not in output_hash:
        output_hash[row[27]] = []
    output_hash[row[27]].append(row[36:612])
    if row[27] == '0_wopBSgNhc':
        prettyprint(row[36:612])

print("overlay array below")

for ytid in output_hash:
    current_row = []
    current_row.append(ytid)

    current_video = output_hash[ytid]

    for second in current_video:
        for row in range(18):
            for col in range(32):
                overlay_array[row][col] = int(second[(32*row) + col])
        if ytid == '0_wopBSgNhc':
            prettyprintoverlay(overlay_array)

        top_level = -1
        row_sum = 0
        while row_sum == 0:
            top_level += 1
            row_sum = sum(overlay_array[top_level])


        bottom_level = 18
        row_sum = 0
        while row_sum == 0:
            bottom_level -= 1
            row_sum = sum(overlay_array[bottom_level])
            


        left_level = -1
        col_sum = 0
        while col_sum == 0:
            left_level += 1
            col_sum = sum(overlay_array[:, left_level])


        right_level = 32
        col_sum = 0
        while col_sum == 0:
            right_level -= 1
            col_sum = sum(overlay_array[:, right_level])
        

        bottom_level += 1
        right_level += 1



        top_left_xy = (((top_level * 20) + 1 ), ((left_level * 20) + 1))
        top_right_xy = (((top_level * 20) + 1 ), (right_level * 20))
        bottom_left_xy = ((bottom_level * 20), ((left_level * 20) + 1))
        bottom_right_xy = ((bottom_level * 20), (right_level * 20))
        current_row.append(top_left_xy)
        current_row.append(top_right_xy)
        current_row.append(bottom_left_xy)
        current_row.append(bottom_right_xy)


    writer.writerow(current_row)


   
    


