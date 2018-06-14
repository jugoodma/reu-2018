import csv
import itertools
import re

# begin
name = 'test.csv' # change this if you want a NEW csv
interval = 1.0
window = 1.0
labels_file = 'class_labels_indices.csv'
data_file = 'unbalanced_train_segments.csv'
start_row = 3
num_rows = 250 # (250) this shouldn't change due to batch limitations in MTurk
labels = {}

print('Creating csv ' + name + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

# create dictionary for mapping obscured labels to human-readable labels
with open(labels_file, newline = '') as f:
    reader = csv.reader(f)
    next(reader) # skip the first line since it has headers for the columns
    for row in reader:
        labels[row[1]] = row[2]

# create csv file with clips
with open('data/' + name, 'w', newline = '') as output:
    writer = csv.writer(output, delimiter = ',', quotechar = '"')
    # write the header row
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['labels'])
    # read data in specified range
    with open(data_file, newline = '') as f:
        reader = itertools.islice(csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True), start_row, start_row + num_rows)
        for row in reader:
            # the following is specific to the .csv files given by AudioSet
            lbls = ', '.join(list(map(lambda l: labels[l],row[3].split(','))))
            ytid = re.search('(=?)(.*)$', row[0]).group(2)
            for i in range(int(((float(row[2]) - float(row[1]) - window) / interval) + 1)): # calculate number of clips
                writer.writerow([ytid] + [int(interval * i + float(row[2]))] + [int(interval * i + window + float(row[2]))] + [lbls])

# end
print('Done.')
