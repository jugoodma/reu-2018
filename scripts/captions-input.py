import random
import json
import csv
import math
import requests
import time
#from multiprocessing import Pool, TimeoutError
from settings import *

start = 0
sub = 0
end = 0
msrvtt = 'videodatainfo_2017.json'
#msrvtt = 'test_videodatainfo_2017.json'
#audioset = 'unbalanced_train_segments.csv'
# switching to AVE dataset, a subset of audioset
#sound = 'msr-vtt-sound.csv' # these are the videos in msr-vtt that have sound
sound = 'msrvtt-train-sound.csv' # list of video IDs from msr-vtt
ran = 'audio-video-dataset.json'

# number of videos per category to skip
# started with 1 video per category
# 7/3 running 10 videos per category
# 7/5 running 10 videos per category
#skip = 11
# stopping the skip

# audioset categories
#cats = ['/m/09x0r', '/m/07yv9'] # 'Speech', 'Vehicle'

print("Creating audio input from msr-vtt...")
start = time.time()

# number of vids per category
# we have a total of 20 categories
#num_vids = 10
# doing all the videos now

# random sampling - seed is for replicatability
random.seed(6942069)

print("Gathering msrvtt vids")
# gather all videos with sound and videos that have not been ran before
r = [x['ytid'] for x in json.load(open(data_path + ran))['data']]
s = list(csv.reader(open(data_path + sound, 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True))
videos = [x for x in json.load(open(data_path + msrvtt))['videos'] if (not x['url'].split('=')[1] in r) and ([x['video_id']] in s)]

# go through each video in the json, only adding videos with sound AND videos that have not been ran before
output = []
print(len(videos))
for vid in videos:
    output.append([vid['url'].split('=')[1]]+[vid['start time']]+[vid['end time']]+['msrvtt'])

random.shuffle(output)
output = output[:626] # change this number for number of outputs
print(len(output))

''' # skipping audioset for now
print("Gathering audioset vids. These ids below are already contained in msrvtt")
# add audioset videos
temp = []
slic = [output[i][0] for i in range(len(output))]
with open(data_path + audioset, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for i in range(3):
        next(reader)
    for row in reader:
        spl = row[3].split(',')
        if (cats[0] in spl or cats[1] in spl):
            if float(row[2]) - float(row[1]) >= 10:
                if row[0] not in slic:
                    temp.append([row[0]]+[int(float(row[1]))]+[int(float(row[2]))])
                else:
                    print(row[0])

# shuffle audioset vids
random.shuffle(temp)
while len(output) < 6000: # only enough money for 5000 videos :'(
    output.append(temp.pop(0))
'''

print("Writing final output file")
# write final output file
with open(input_path + environments['captions']['csv'], 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # write the header
    writer.writerow(['ytid'] + ['start'] + ['end']+ ['origin'])
    writer.writerows(output)

# done
print("Done.")

