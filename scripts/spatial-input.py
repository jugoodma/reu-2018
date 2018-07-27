import csv
from settings import *

# begin
interval = 1.0
window = 1.0
final_data = environments['spatial']['csv']
#audioset = 'unbalanced_train_segments.csv'
# this subset file needs rows as follows:
# [ label, youtube id, ave start time, ave end time ]
# and no header
# and separated by & not ,
subset = input("subset file: ../data/")

print('Creating csv ' + final_data + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

# put all rows from subset into temp list
with open(data_path + subset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = '&', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    temp = list(reader)

# create mturk input csv
with open(input_path + final_data, 'w', newline = '') as f:
    writer = csv.writer(f,  quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # write the header row
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['label'])
    for row in temp:
        offset = 0
        for i in range(int(((float(row[4]) - float(row[3]) - window) / interval) + 1)): # calculate number of clips
            r = [row[1]] + [int((interval * i) + int(row[3])) + offset] + [int((interval * i) + window + int(row[3])) + offset] + [row[0]]
            print(r)
            writer.writerow(r)

# end
print('Done.')
