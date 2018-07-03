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
ontology = 'ontology.json'
audioset = 'unbalanced_train_segments.csv'
final_data = environments['temporal']['csv']
labels = {} # and descriptions
usable_videos = {}
# the amount of videos you want per category from the list of top 25 categories
amount_per_category = 10

# set random seed for reproductability
random.seed(6942069)

# skip amount (started at 1)
# 6/26 running 20 videos per category
# 6/27 running 1 video per category
# 6/28 running 4 video per category
# 7/3 running 10 videos per category
skip = 30

print('Creating csv ' + final_data + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window.')

# the categories we want to run
category_list = ['Music', 'Speech', 'Vehicle', 'Singing', 'Car', 'Animal', 'Outside, rural or natural', 'Bird', 'Engine', 'Child speech, kid speaking', 'Water', 'Siren', 'Tools', 'Bird vocalization, bird call, bird song', 'Wind instrument, woodwind instrument', 'Laughter', 'Cheering', 'Gunshot, gunfire', 'Radio', 'Fireworks', 'Stream', 'Snoring', 'Explosion', 'Bell', 'Oink']
print(len(category_list))

# create dictionary for mapping obscured labels to human-readable labels + descriptions
with open(data_path + ontology, 'r', encoding='latin-1') as json_data:
    data = json.load(json_data)
    for obj in data:
        if obj['name'] in category_list:
            labels[obj['id']] = {'name': obj['name'], 'description': obj['description'],}
print(labels)

# comment
with open(data_path + audioset, 'r', newline = '') as f:
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
        google_labels = row[3].split(',')
        english_label = labels.get(google_labels[0])
        if len(google_labels) < 2 and english_label:
            usable_videos[english_label['name']].append([row[0], row[1], row[2], english_label['name'], english_label['description']])

# comment
with open(data_path + final_data, 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['label'] + ['description'])
    # sample <amount_per_category> number of random videos from usable_videos
    for key in usable_videos:
        # skip some
        for count in range(skip):
            row = random.choice(usable_videos[key])
            usable_videos[key].remove(row)
        # write videos
        for count in range(amount_per_category):
            row = random.choice(usable_videos[key])
            usable_videos[key].remove(row)
            row[1] = int(float(row[1]))
            row[2] = int(float(row[2]))
            print(row)
            writer.writerow(row)

print('Done.')
