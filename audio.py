import random
import json
import csv
import math
from settings import *

msrvtt = 'videodatainfo_2017.json'
# number of videos per category to skip
# started with 1 video per category
# 7/3 running 10 videos per category
skip = 1

print("Creating audio input from msr-vtt...")
# number of vids per category
# we have a total of 20 categories
num_vids = 10

# random sampling - seed is for replicatability
random.seed(6942069)

# generate temp data structure
temp = []
for i in range(20):
    temp.append([])
# go through each video in the json and add it to the temp data structure
videos = json.loads(open(data_path + msrvtt).read())['videos']
for vid in videos:
    ytid = vid['url'].split('=')[1]
    temp[vid['category']].append([ytid]+[math.ceil(vid['start time'])]+[math.floor(vid['end time'])]+[vid['category']])
# write final output file
with open(data_path + environments['audio']['csv'], 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # write the header
    writer.writerow(['ytid'] + ['start'] + ['end'] + ['category'])
    # shuffle each category and choose num_vids from the top
    for i in range(20):
        random.shuffle(temp[i])
        count = skip # 0 + skip
        while count < num_vids + skip and count < len(temp[i]):
            writer.writerow(temp[i][count])
            count += 1

# done
print("Done.")
