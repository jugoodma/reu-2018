import csv
import random
from settings import *

# begin
interval = 1.0
window = 1.0
final_data = environments['spatial']['csv']
audioset = 'unbalanced_train_segments.csv'
subset = 'spatial-sub.csv'

print('Creating csv ' + final_data + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

random.seed(6942069)

# create csv file with clips
temp = []
with open(data_path + subset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = '&', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for row in reader:
        temp.append(row)
#random.shuffle(temp)
#temp = temp[0:20]
starts = {}
"""
with open(data_path + audioset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for i in range(3):
        next(reader)
    for row in reader:
        starts[row[0]] = [int(float(row[1])), int(float(row[2]))] # start, end
"""
with open(data_path + final_data, 'w', newline = '') as f:
    writer = csv.writer(f,  quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # write the header row
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['label'])
    for row in temp:
        #offset = starts[row[1]][0] # when using YouTube and not the actual .mp4 files
        offset = 0
        for i in range(int(((float(row[4]) - float(row[3]) - window) / interval) + 1)): # calculate number of clips
            r = [row[1]] + [int((interval * i) + int(row[3])) + offset] + [int((interval * i) + window + int(row[3])) + offset] + [row[0]]
            print(r)
            writer.writerow(r)

# end
print('Done.')
