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
labels_file = 'class_labels_indices.csv'
original_data = 'unbalanced_train_segments.csv'
final_data = environments['temporal']['csv']
labels = {}
usable_videos = {}
amount_per_category = 1 # the amount of videos you want per category from the list of top 25 categories

# set random seed for reproductability
random.seed(6942069)

print('Creating csv ' + final_data + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

#category_list = (('Music', 0), ('Speech', 0), ('Vehicle', 0), ('Musical instrument', 0), ('Plucked string instrument', 0), ('Singing',0), ('Car', 0), ('Animal', 0), ('Outside, rural or natural', 0), ('Bird', 0), ('Drum', 0), ('Engine', 0), ('Narration, monologue', 0), ('Drum kit', 0), ('Dog', 0), ('Child speech, kid speaking', 0), ('Bass drum', 0), ('Rail transport', 0), ('Motor vehicle (road)', 0), ('Water', 0), ('Siren', 0), ('Tools', 0), ('Railroad car, train wagon', 0), ('Snare drum', 0), ('Bird vocalization, bird call, bird song', 0))

# the categories we want to run
category_list = ['Music', 'Speech', 'Vehicle', 'Singing', 'Car', 'Animal', 'Outside, rural or natural', 'Bird', 'Engine', 'Narration, monologue', 'Child speech, kid speaking', 'Water', 'Siren', 'Tools', 'Bird vocalization, bird call, bird song', 'Wind instrument, woodwind instrument', 'Cheering', 'Gunshot, gunfire', 'Radio', 'Fireworks', 'Stream', 'Snoring', 'Explosion', 'Bell', 'Oink']
print(len(category_list))

# create dictionary for mapping obscured labels to human-readable labels
with open(data_path + labels_file, newline = '') as f:
    reader = csv.reader(f)
    next(reader) # skip the first line since it has headers for the columns
    for row in reader:
        labels[row[1]] = row[2]

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
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['labels'])
    # sample <amount_per_category> number of random videos from usable_videos
    for key in usable_videos:
        for count in range(amount_per_category):
            row = random.choice(usable_videos[key])
            usable_videos[key].remove(row)
            row[1] = int(float(row[1]))
            row[2] = int(float(row[2]))
            print(row)
            writer.writerow(row)

print('Done.')
