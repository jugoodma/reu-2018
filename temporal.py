import csv
import itertools
import re
import json
import math
import requests
from settings import *
import random
# begin
data_path = 'data/'
ave = 'ave.csv'
name = 'temporal-input.csv'
interval = 1.0
window = 1.0
labels_file = 'class_labels_indices.csv'
data_file = 'temp.csv'
original_data = 'unbalanced_train_segments.csv'
final_data = environments['temporal']['csv']
start_row = 3
num_rows =  5000# (250) this shouldn't change due to batch limitations in MTurk
labels = {}
usable_videos = {}
amount_per_category = 250 # the amount of videos you want per category from the list of top 25 categories


print('Creating csv ' + name + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

#category_list = (('Music', 0), ('Speech', 0), ('Vehicle', 0), ('Musical instrument', 0), ('Plucked string instrument', 0), ('Singing',0), ('Car', 0), ('Animal', 0), ('Outside, rural or natural', 0), ('Bird', 0), ('Drum', 0), ('Engine', 0), ('Narration, monologue', 0), ('Drum kit', 0), ('Dog', 0), ('Child speech, kid speaking', 0), ('Bass drum', 0), ('Rail transport', 0), ('Motor vehicle (road)', 0), ('Water', 0), ('Siren', 0), ('Tools', 0), ('Railroad car, train wagon', 0), ('Snare drum', 0), ('Bird vocalization, bird call, bird song', 0))


category_list = ['Music', 'Speech', 'Vehicle', 'Singing', 'Car', 'Animal', 'Outside, rural or natural', 'Bird', 'Engine', 'Narration, monologue', 'Child speech, kid speaking', 'Water', 'Siren', 'Tools', 'Bird vocalization, bird call, bird song', 'Wind instrument, woodwind instrument', 'Cheering', 'Gunshot, gunfire', 'Radio', 'Fireworks', 'Stream', 'Snoring', 'Explosion', 'Bell', 'Oink']
print(len(category_list))

# create dictionary for mapping obscured labels to human-readable labels
with open(data_path + labels_file, newline = '') as f:
    reader = csv.reader(f)
    next(reader) # skip the first line since it has headers for the columns
    for row in reader:
        labels[row[1]] = row[2]



output = open(data_path + data_file, newline = '')

ave_reader = csv.reader(open(data_path + ave, 'r', newline = ''), quotechar = '"', delimiter = '&', quoting = csv.QUOTE_ALL, skipinitialspace = True)
reader = csv.reader(open(data_path + original_data, 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
writer = csv.writer(open(data_path + data_file, 'w', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)

for i in range(len(category_list)):
    x = []
    usable_videos[category_list[i]] = x


for j in range(3):
    next(reader)

for row in reader:
    matches = False
    google_labels = row[3].split(',')
    if len(google_labels) < 2:
        english_label = labels[google_labels[0]]
        if english_label in category_list:
            usable_videos[english_label].append([row[0], row[1], row[2], english_label])


for key in usable_videos:
    count = 0
    while count < amount_per_category:
        the_row = random.choice(usable_videos[key])
        print(the_row)
        writer.writerow(the_row)
        count += 1
        usable_videos[key].remove(the_row)




"""
with open(data_path + original_data, newline = '') as unbalanced:
    read = csv.reader(unbalanced, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for row in reader:
"""



# create csv file with clips
with open(data_path + final_data, 'w', newline = '') as output:
    writer = csv.writer(output, delimiter = ',', quotechar = '"')
    # write the header row
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['labels'])
    # read data in specified range
    with open(data_path + data_file, newline = '') as f:
        reader = itertools.islice(csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True), start_row, start_row + num_rows)
        for row in reader:
            # the following is specific to the .csv files given by AudioSet
            #lbls = ', '.join(list(map(lambda l: labels[l], row[3].split(','))))
            for i in range(int(((float(row[2]) - float(row[1]) - window) / interval) + 1)): # calculate number of clips
                writer.writerow([row[0]] + [int(interval * i + float(row[2]))] + [int(interval * i + window + float(row[2]))] + [row[3]])

"""

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
