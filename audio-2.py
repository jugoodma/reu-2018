import random
import csv
from settings import *

# number of vids per category
num_vids = 50

# random sampling - seed is for replicatability
random.seed(123456)

# load up the MSR-VTT data
lines = open(data_path + "msr_exists.csv", "r").readlines()

# generate the temporary data structure
videos = []
for i in range(20):
    videos.append([])

# shuffle the rows in the 
# if exists, add to data structure
for line in lines:
    # line structure is:
    # "ytid,start,end,category\n"
    row = line.split(",")
    cat = int(row[3])
    if len(videos[cat]) < num_vids:
        videos[cat].append(row)

for i in videos:
    print(len(videos[i]))


