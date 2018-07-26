import csv
import numpy
import itertools
from settings import *

input_data = input("filename: ./")
output_data = 'spatial-batch-output-parsed.csv'

# row[36] first location row[612] last location
# ^ this is from amazon directly.
#
# new frontend acceptance tool outputs .csv as follows:
# ID,YTID,response0,...,response575
#
# look in the history of this repo to see how we did it originally
#

# helpers for debugging
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


# read in and sort data
def k(lst):
    return lst[0], lst[1]

output = []
with open(input_data, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for row in reader:
        output.append([row[1][:11], int(row[1][12])] + row[2:579])

output.sort(key = k)

# write final output
with open(data_path + output_data, 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)

    # header row for final output
    templist = []
    templist.append('ytid')
    for i in range(10):
        templist.append('second' + str(i+1))
        for i in range(3):
            templist.append('')
    writer.writerow(templist)

    overlay_array = numpy.zeros((18, 32)) # arr to store the response
    output_hash = {} # hash to contain ytid -> [second 0, second 1, ...]

    # fill in hash
    for row in output:
        if row[0] not in output_hash:
            output_hash[row[0]] = []
        output_hash[row[0]].append(row[2:])

    # go through each ytid in hash
    for ytid in output_hash:
        current_row = []
        current_row.append(ytid)

        # go through each second (576 response array) and calculate bounding box
        for second in output_hash[ytid]:
            # 1. fill in numpy array so we can easily work
            for row in range(18):
                for col in range(32):
                    overlay_array[row][col] = int(second[(32*row) + col])

            # 2. calculate each side of the bounding box
            # top
            top_level = -1
            row_sum = 0
            while row_sum == 0:
                top_level += 1
                row_sum = sum(overlay_array[top_level])

            # bottom
            bottom_level = 18
            row_sum = 0
            while row_sum == 0:
                bottom_level -= 1
                row_sum = sum(overlay_array[bottom_level])

            # left
            left_level = -1
            col_sum = 0
            while col_sum == 0:
                left_level += 1
                col_sum = sum(overlay_array[:, left_level])

            # right
            right_level = 32
            col_sum = 0
            while col_sum == 0:
                right_level -= 1
                col_sum = sum(overlay_array[:, right_level])

            # adjust the bottom and right layer
            bottom_level += 1
            right_level += 1

            # pretty print debug example:
            """
            if ytid == '-6TQKeeULa0':
                print("top    : " + str(top_level))
                print("bottom : " + str(bottom_level))
                print("left   : " + str(left_level))
                print("right  : " + str(right_level))
                print("second: ")
                prettyprint(second)
            """

            # 3. append the current second to the current row
            top_left_xy = (((top_level * 20) + 1 ), ((left_level * 20) + 1))
            top_right_xy = (((top_level * 20) + 1 ), (right_level * 20))
            bottom_left_xy = ((bottom_level * 20), ((left_level * 20) + 1))
            bottom_right_xy = ((bottom_level * 20), (right_level * 20))
            current_row.append(top_left_xy)
            current_row.append(top_right_xy)
            current_row.append(bottom_left_xy)
            current_row.append(bottom_right_xy)

        # all seconds are calculated, now append row to writer
        writer.writerow(current_row)
