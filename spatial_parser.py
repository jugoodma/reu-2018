import csv
import numpy
import itertools

input_data = 'spatial-batch-output.csv'

output_data = './data/spatial-batch-output-parsed.csv'
temp_data = './data/tempt_data.csv'
#row[36] first location row[612] last location

reader = csv.reader(open(input_data, 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)

writer = csv.writer(open(output_data, 'w', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)


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

pixel_array = numpy.zeros((640, 360))

overlay_array = numpy.zeros((18, 32))

def compare(lst):
    return lst[27], lst[28]

output = []

for row in reader:
    output.append(row)

output.sort(key = compare)


output_hash = {}

for row in output:
    if row[27] not in output_hash:
        output_hash[row[27]] = []
    output_hash[row[27]].append(row[36:612])


for ytid in output_hash:
    current_row = []
    current_row.append(ytid)

    current_video = output_hash[ytid]

    for second in current_video:
        for row in range(18):
            for col in range(32):
                overlay_array[row][col] = int(second[(32*row) + col])


        top_level = 0
        row_sum = 0
        while row_sum == 0:
            
            row_sum = sum(overlay_array[top_level])
            if row_sum == 0:
                top_level += 1


        bottom_level = 17
        row_sum = 0
        while row_sum == 0:

            row_sum = sum(overlay_array[bottom_level])
            if row_sum == 0:
                bottom_level -= 1


        left_level = 0
        col_sum = 0
        while col_sum == 0:
            col_sum = sum(overlay_array[:, left_level])
            if col_sum == 0:
                left_level += 1


        right_level = 31
        col_sum = 0
        while col_sum == 0:
            col_sum = sum(overlay_array[:, right_level])
            if col_sum == 0:
                right_level -= 1


        top_level += 1
        right_level += 1
        left_level += 1
        bottom_level +=1


        top_left_xy = (((top_level * 20) + 1 ), ((left_level * 20) + 1))
        top_right_xy = (((top_level * 20) + 1 ), (right_level * 20))
        bottom_left_xy = ((bottom_level * 20), ((left_level * 20) + 1))
        bottom_right_xy = ((bottom_level * 20), (right_level * 20))
        current_row.append(top_left_xy)
        current_row.append(top_right_xy)
        current_row.append(bottom_left_xy)
        current_row.append(bottom_right_xy)


    writer.writerow(current_row)


   
    


