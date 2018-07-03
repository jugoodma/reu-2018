import csv
import itertools
import re
import json
import math
import requests
from settings import *
import random
# begin
interval = 1.0
window = 1.0
labels_file = 'ontology.json'
original_data = 'unbalanced_train_segments.csv'
final_data = environments['temporal']['csv']
labels = {}
usable_videos = {}
# the amount of videos you want per category from the list of top 25 categories
amount_per_category = 4

# set random seed for reproductability
random.seed(6942069)

# skip amount (started at 1)
# 6/26 running 20 videos per category
# 6/27 running 1 video per category
# 6/28 running 4 video per category
skip = 23

print('Creating csv ' + final_data + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

# the categories we want to run
category_list = ['Music', 'Speech', 'Vehicle', 'Singing', 'Car', 'Animal', 'Outside, rural or natural', 'Bird', 'Engine', 'Child speech, kid speaking', 'Water', 'Siren', 'Tools', 'Bird vocalization, bird call, bird song', 'Wind instrument, woodwind instrument', 'Laughter', 'Cheering', 'Gunshot, gunfire', 'Radio', 'Fireworks', 'Stream', 'Snoring', 'Explosion', 'Bell', 'Oink']
print(len(category_list))

# create dictionary for mapping obscured labels to human-readable labels
with open(data_path + labels_file).read() as json_data:
    data = json.loads(json_data)
         # skip the first line since it has headers for the columns
    for row in reader:
        labels[] = row[2]

# comment
with open(data_path + original_data, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # create usable_video datastructure
    for i in range(len(category_list)):
        x = []
        usable_videos[category_list[i]] = x
    # skip the three header comments in AudioSet
    for j in range(3):
        next(reader)
    # check each AudioSet video for a few things
    # 1 - the number of labels for the video must be 1
    # 2 - the label must be in our categories list
    for row in reader:
        matches = False
        google_labels = row[3].split(',')
        if len(google_labels) < 2:
            english_label = labels[google_labels[0]]
            if english_label in category_list:
                usable_videos[english_label].append([row[0], row[1], row[2], english_label])

# comment
with open(data_path + final_data, 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['label'] + ['description'])
    # sample <amount_per_category> number of random videos from usable_videos
    for key in usable_videos:
        for count in range(skip):
            row = random.choice(usable_videos[key])
            usable_videos[key].remove(row)
        for count in range(amount_per_category):
            row = random.choice(usable_videos[key])
            usable_videos[key].remove(row)
            row[1] = int(float(row[1]))
            row[2] = int(float(row[2]))
            print(row)
            writer.writerow(row)

print('Done.')
