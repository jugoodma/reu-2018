import csv
import itertools
import re
import json
import math
import requests

# begin
data_path = 'data/'
name = 'temporal-input.csv'
interval = 1.0
window = 1.0
labels_file = 'class_labels_indices.csv'
data_file = 'unbalanced_train_segments_trimmed.csv'
original_data = 'unbalanced_train_segments.csv'
start_row = 3
num_rows =  5000# (250) this shouldn't change due to batch limitations in MTurk
labels = {}

print('Creating csv ' + name + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

category_list = ('Music', 'Speech', 'Vehicle', 'Musical instrument', 'Plucked string instrument', 'Singing', 'Car', 'Animal', 'Outside, rural or natural', 'Bird', 'Drum', 'Engine', 'Narration, monologue', 'Drum kit', 'Dog', 'Child speech, kid speaking', 'Bass drum', 'Rail transport', 'Motor vehicle (road)', 'Water', 'Siren', 'Tools', 'Railroad car, train wagon', 'Snare drum', 'Bird vocalization, bird call, bird song')


# create dictionary for mapping obscured labels to human-readable labels
with open(data_path + labels_file, newline = '') as f:
    reader = csv.reader(f)
    next(reader) # skip the first line since it has headers for the columns
    for row in reader:
        labels[row[1]] = row[2]



output = open(data_path + data_file, newline = '')

reader = csv.reader(open(data_path + original_data, 'r', newline = ''), delimiter = ",", quotechar = '"')

for j in range(3):
    next(reader)

for row in reader:
    google_labels = row[3].split(',')
    google_labels = google_labels[0]
    google_labels = labels[google_labels]
    for i in range(len(category_list)):
        if google_labels == category_list[i]:
            print("matches")



"""
with open(data_path + original_data, newline = '') as unbalanced:
    read = csv.reader(unbalanced, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for row in reader:
"""



# create csv file with clips
with open(data_path + name, 'w', newline = '') as output:
    writer = csv.writer(output, delimiter = ',', quotechar = '"')
    # write the header row
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['labels'])
    # read data in specified range
    with open(data_path + data_file, newline = '') as f:
        reader = itertools.islice(csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True), start_row, start_row + num_rows)
        for row in reader:
            # the following is specific to the .csv files given by AudioSet
            lbls = ', '.join(list(map(lambda l: labels[l],row[3].split(','))))
            for i in range(int(((float(row[2]) - float(row[1]) - window) / interval) + 1)): # calculate number of clips
                writer.writerow([row[0]] + [int(interval * i + float(row[2]))] + [int(interval * i + window + float(row[2]))] + [lbls])

"""import json
import csv
import math
import requests


msr = open('videodatainfo_2017.json')

msr_json_parsed = json.loads(msr.read())

msr_data_videos = msr_json_parsed['videos']

# open a file for writing

msr_csv = open('msr_csv.csv', 'a')

# create the csv writer object

csvwriter = csv.writer(msr_csv)
header = ['ytid', 'start_time', 'end_time', 'category']
csvwriter.writerow(header)

for row in msr_data_videos:
    ytid = row['url']
    ytid = ytid.split('=')
    ytid = ytid[1]

    url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=AIzaSyAZUmdgun5Ao9D2kz43MxrCGOKkqsYsfFU&part=status' % ytid
    url_get = requests.get(url)
    
    if len(url_get.json()['items']) != 0:
        start_t = math.floor(row['start time'])

        end_t = math.ceil(row['end time'])

        category = row['category']

        row_string = (ytid, start_t, end_t, category)

        csvwriter.writerow(row_string)
        """

# end
print('Done.')
