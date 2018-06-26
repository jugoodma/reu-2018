import random
import json
import csv
import math
from settings import *

'''
# this code creates a csv file of MSR-VTT videos that are playable on YouTube
yes = input("This will use about 20,000 requests with your YouTube data v3 API credentials. You should not do this if the data file already exists. Are you sure you want to continue? (y/n):")

if yes == 'y':
    output = 'msr-exists.csv'

    print("Validating the existance of each video in MSR-VTT. This will take a while. Output is in " + data_path + output + " ...")

    # read in the videos
    videos = json.loads(open(data_path + "videodatainfo_2017.json").read())['videos']

    # create the csv writer object
    writer = csv.writer(open(data_path + output, 'w'))

    # write header row
    writer.writerow(['ytid', 'start', 'end', 'category'])

    # go thru each video and check if it exists
    # if it exists, put it in the csv
    for vid in videos:
        print(vid)
        # ytid is in known location for every video url
        ytid = vid['url'].split('=')[1]
        if youtube_video_exists(ytid):
            writer.writerow([ytid]+[math.floor(vid['start time'])]+[math.ceil(vid['end time'])]+[vid['category']])
'''

print("Creating audio input from msr-vtt...")
# number of vids per category
# we have a total of 20 categories
num_vids = 1

# random sampling - seed is for replicatability
random.seed(6942069)

# generate temp data structure
temp = []
for i in range(20):
    temp.append([])
# go through each video in the json and add it to the temp data structure
videos = json.loads(open(data_path + "videodatainfo_2017.json").read())['videos']
for vid in videos:
    ytid = vid['url'].split('=')[1]
    temp[vid['category']].append([ytid]+[math.ceil(vid['start time'])]+[math.floor(vid['end time'])])
# write final output file
with open(data_path + environments['audio']['csv'], 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # write the header
    writer.writerow(['ytid'] + ['start'] + ['end'])
    # shuffle each category and choose num_vids from the top
    for i in range(20):
        random.shuffle(temp[i])
        count = 0
        while count < num_vids and count < len(temp[i]):
            writer.writerow(temp[i][count])
            count += 1

# done
print("Done.")
