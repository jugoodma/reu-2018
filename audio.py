import random
import json
import csv
import math
import requests
import time
from multiprocessing import Pool, TimeoutError
from settings import *

start = 0
sub = 0
end = 0
msrvtt = 'videodatainfo_2017.json'
audioset = 'unbalanced_train_segments.csv'
sound = 'msr-vtt-sound.csv' # these are the videos in msr-vtt that have sound
ytdirect = 'https://you-link.herokuapp.com/?url=https://www.youtube.com/watch?v='
# number of videos per category to skip
# started with 1 video per category
# 7/3 running 10 videos per category
# 7/5 running 10 videos per category
#skip = 11
# stopping the skip

# audioset categories
cats = ['/m/09x0r', '/m/07yv9'] # 'Speech', 'Vehicle'

print("Creating audio input from msr-vtt...")
start = time.time()

# number of vids per category
# we have a total of 20 categories
#num_vids = 10
# doing all the videos now

# random sampling - seed is for replicatability
random.seed(6942069)

print("Gathering msrvtt vids")
# gather all videos with sound
temp = []
with open(data_path + sound, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    for row in reader:
        temp.append(row[0])

# go through each video in the json, only adding videos with sound
output = []
videos = json.loads(open(data_path + msrvtt).read())['videos']
for vid in videos:
    if vid['video_id'] in temp:
        ytid = vid['url'].split('=')[1]
        output.append([ytid]+[vid['start time']]+[vid['end time']]+['msrvtt'])
random.shuffle(output)
output = output[:5001]

print(round(time.time() - start, 4))
sub = time.time()

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
print(round(time.time() - sub, 4))
sub = time.time()

print("Writing final output file")
# write final output file
with open(data_path + environments['audio']['csv'], 'w', newline = '') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    # write the header
    writer.writerow(['ytid'] + ['start'] + ['end']+ ['origin'])
    writer.writerows(output)

print(round(time.time() - sub, 4))
end = time.time()
print("Total time: " + str(round(end - start, 4)))
# done
print("Done.")
