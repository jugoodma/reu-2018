import csv
import itertools
import re
import json
import math
import requests
import random
from settings import *

# begin
interval = 1.0
window = 1.0
ontology = 'ontology.json'
audioset = 'unbalanced_train_segments.csv'
final_data = environments['temporal']['csv']
labels = {} # and descriptions
usable_videos = {}
# the amount of videos you want per category from the list of top 25 categories
amount_per_category = 200

# set random seed for reproductability
random.seed(6942069)

# the categories we want to run
"""
category_list = ['Child speech, kid speaking',
                 'Radio',
                 'Stream',
                 'Snoring',
                 'Computer keyboard',
                 'Oink',
                 'Tick',
                 'Sneeze',
                 'Motorboat, speedboat',
                 'Choir',
                 'Vacuum cleaner',
                 'Sewing machine',
                 'Walk, footsteps',
                 'Ringtone',
                 'Buzzer',
                 'Fire alarm',
                 'Microwave oven',
                 'Change ringing (campanology)',
                 'Waves, surf',
                 'Clarinet',
                 'Accelerating, revving, vroom',
                 'Printer',
                 'Skateboard',
                 'Blender',
                 'Lawn mower']
"""

# create dictionary for mapping obscured labels to human-readable labels + descriptions
with open(data_path + ontology, 'r', encoding='latin-1') as json_data:
    data = json.load(json_data)
    for obj in data:
        if len(obj['child_ids']) == 0:
            labels[obj['id']] = {'name': obj['name'], 'description': obj['description'],}
            usable_videos[obj['name']] = []

with open(data_path + audioset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # skip the three header comments in AudioSet
    for j in range(3):
        next(reader)
    # check each AudioSet video for a few things
    # 1 - the number of labels for the video must be 1
    for row in reader:
        google_labels = row[3].split(',')
        english_label = labels.get(google_labels[0])
        if len(google_labels) < 2 and english_label:
            usable_videos[english_label['name']].append([row[0], row[1], row[2], english_label['name'], english_label['description']])

# comment
for key in usable_videos:
    l = len(usable_videos[key])
    if l >= 200:
        print(key + ": " + str(l))
