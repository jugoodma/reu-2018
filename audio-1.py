import json
import csv
import requests
import math
from settings import *

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

print("Done.")
