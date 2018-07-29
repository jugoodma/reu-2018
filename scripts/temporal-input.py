# this script generates an input .csv file for
# amazon mturk temporal annotator
# categories are based on your input
# first argument to script is number of videos per category

# imports
import sys
import random
import csv
import re
import json
import math
import requests
from settings import *

# initial variables
cat_list = 'temporal-input-labels.txt'
ontology = 'ontology.json'
audioset = 'unbalanced_train_segments.csv'
final_data = environments['temporal']['csv']
amount_per_category = (200 if len(sys.argv) < 2 else int(sys.argv[1]))

# set random seed for reproductability
random.seed(6942069)

print('Creating csv ' + final_data)

# read in each category (human-readable)
category_list = [x.rstrip() for x in open(data_path + cat_list)]
print(len(category_list))

# create dictionary for mapping obscured labels to human-readable labels + descriptions
labels = {} # and descriptions
with open(data_path + ontology, 'r', encoding='latin-1') as json_data:
    data = json.load(json_data)
    for obj in data:
        if obj['name'] in category_list:
            labels[obj['id']] = {'name': obj['name'], 'description': obj['description'],}
print(labels)

# go through audioset and pick out usable videos
usable_videos = {}
usable_twolabels = {}
with open(data_path + audioset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # create usable_video structures
    for i in range(len(category_list)):
        usable_videos[category_list[i]] = []
        usable_twolabels[category_list[i]] = []
    # skip the three header comments in AudioSet
    for j in range(3):
        next(reader)
    # check each AudioSet video for a few things
    # 1 - the number of labels for the video must be 1 or 2
    # 2 - the label must be in our categories list
    # i'm too lazy to optimize this
    for row in reader:
        google_labels = row[3].split(',')
        glen = len(google_labels)
        if glen < 2:
            english_label = labels.get(google_labels[0])
            if english_label:
                usable_videos[english_label['name']].append([row[0], row[1], row[2], english_label['name'], english_label['description']])
        elif glen < 3:
            # first label in list gets priority
            english_label = labels.get(google_labels[0])
            if english_label:
                usable_twolabels[english_label['name']].append([row[0], row[1], row[2], english_label['name'], english_label['description']])
            else:
                english_label = labels.get(google_labels[1])
                if english_label:
                    usable_twolabels[english_label['name']].append([row[0], row[1], row[2], english_label['name'], english_label['description']])

# go through each video in our usable videos category, shuffle the videos and generate final .csv
# priority 1 is selecting all 1-label videos
# priority 2 is selecting from the 2-label videos
with open(input_path + final_data, 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['label'] + ['description'])
    # sample <amount_per_category> number of random videos from usable_videos
    for key in usable_videos:
        print(key)
        print(len(usable_videos[key]))
        print(len(usable_twolabels[key]))
        
        if len(usable_videos[key]) < amount_per_category:
            random.shuffle(usable_twolabels[key])
        else:
            random.shuffle(usable_videos[key])
        both = usable_videos[key] + usable_twolabels[key]
        # write videos
        for count in range(amount_per_category):
            row = both[count]
            row[1] = int(float(row[1]))
            row[2] = int(float(row[2]))
            print(row)
            writer.writerow(row)

print('Done.')
