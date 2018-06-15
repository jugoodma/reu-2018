import json
import csv
import math
import requests


msr = open('videodatainfo_2017.json')

msr_json_parsed = json.loads(msr.read())

msr_data_videos = msr_json_parsed['videos']

# open a file for writing

msr_csv = open('msr_csv.csv', 'a')

# create the csv writer object

csvwriter = csv.writer(msr_csv)
header = ['ytid', 'start_time', 'end_time', 'category']
csvwriter.writerow(header)

for row in msr_data_videos:
    ytid = row['url']
    ytid = ytid.split('=')
    ytid = ytid[1]

    url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=AIzaSyAZUmdgun5Ao9D2kz43MxrCGOKkqsYsfFU&part=status' % ytid
    url_get = requests.get(url)
    
    if len(url_get.json()['items']) != 0:
        start_t = math.floor(row['start time'])

        end_t = math.ceil(row['end time'])

        category = row['category']

        row_string = (ytid, start_t, end_t, category)

        csvwriter.writerow(row_string)


    
    

