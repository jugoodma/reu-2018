import csv
import json
import pickle
import math
import os.path
from datetime import datetime
from settings import *

input_data = input("What file would you like to run: ./results/")
dt = input("Which data type is this file? (audio or video): ")
split = input("What split is this file? (test or train or val): ")
origin = input("What origin is this file? (ave or msrvtt): ")

desc = "Separate annotations for both audio and video streams"
today = str(datetime.now())

mcache = "msrvtt.cache"
acache = "audioset.cache"
output = "audio-video-dataset.json"
data = json.load(open(output, 'r'))
msrvtt = json.load(open(data_path + "videodatainfo_2017.json", 'r'))
audioset = csv.reader(open(data_path + "unbalanced_train_segments.csv", 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
r = 50 # number of sentences per video (actual value is 2, but we padded this in case we add to the dataset)

data['info']['description'] = desc
data['info']['data_created'] = today

# audio:
# Audio (blacked out video)
# 

# video:
# Video (muted audio)
# 

# create msrvtt video key-val lookup
vids = {}
if os.path.isfile(data_path + mcache):
    with open(data_path + mcache, 'rb') as f:
        vids = pickle.load(f)
else:
    for obj in msrvtt['videos']:
        ytid = obj['url'].split('=')[1]
        obj.pop('url')
        obj.pop('category')
        obj['ytid'] = ytid
        obj['origin'] = 'msrvtt'
        vids[ytid, math.floor(obj['start time'])] = obj
    with open(data_path + mcache, 'wb') as f:
        pickle.dump(vids, f)

# create audioset video key-val lookup
asvids = {}
if os.path.isfile(data_path + acache):
    with open(data_path + acache, 'rb') as f:
        asvids = pickle.load(f)
else:
    count = 20000 # audioset IDs start at 20,000
    for i in range(3):
        next(audioset)
    for row in audioset:
        ytid = row[0]
        asvids[ytid, int(float(row[1]))] = {'id': count,
                                            'video_id': 'video' + str(count),
                                            'origin': 'audioset',
                                            'ytid': ytid,
                                            'start time': float(row[1]),
                                            'end time': float(row[2]),
                                            'split': 'train'}
        count += 1
    with open(data_path + acache, 'wb') as f:
        pickle.dump(asvids, f)

# our dataset formatting is specified in the README.md

with open(result_path + input_data, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)

    # get indexed locations of the important stuff in the header row
    idx_ytid = -1
    idx_start = -1
    idx_end = -1
    idx_origin = -1
    idx_response = -1
    idx_approval = -1
    idx_err = -1
    for idx, ele in enumerate(next(reader)):
        if ele == "Input.ytid":
            idx_ytid = idx
        elif ele == "Input.start":
            idx_start = idx
        elif ele == "Input.end":
            idx_end = idx
        elif ele == "Input.origin":
            idx_origin = idx
        elif ele == "Answer.response":
            idx_response = idx
        elif ele == "ApprovalTime": # "ApprovalTime"
            idx_approval = idx
        elif ele == "Answer.youtubeError":
            idx_err = idx
        else:
            continue

    # use these indices to append to the data
    for row in reader:
        # we only want approved data
        #   and
        # we only want non-errored data
        if not (row[idx_approval] == "" or row[idx_err] == "1"):
            # get video entry
            v = vids.get((row[idx_ytid], math.floor(float(row[idx_start]))))
            if v is None:
                # could be a floor/ceil error
                v = vids.get((row[idx_ytid], math.floor(float(row[idx_start])) - 1))
            if v is None:
                # video was not in msrvtt, so check audioset
                v = asvids.get((row[idx_ytid], int(float(row[idx_start]))))
            # get data entry
            i = -1
            for idx, obj in enumerate(data['data']):
                if obj['id'] <= v['id']:
                    i = idx
            if i == -1 or not data['data'][i]['id'] == v['id']:
                # data not found, insert new data after this index
                #   or
                # no data, this is the first run
                v['origin'] = origin
                v['split'] = split
                v[dt] = [{'sen_id': str(r * v['id']) + dt[0],
                          'video_id': v['video_id'],
                          'caption': row[idx_response].lower()}]
                v['audio' if dt == 'video' else 'video'] = []
                data['data'].insert(i + 1, v)
            else:
                # data entry found, so edit it
                d = data['data'][i]
                data['data'][i][dt].append({'sen_id': str((r * d['id']) + len(d[dt])) + dt[0],
                                            'video_id': d['video_id'],
                                            'caption': row[idx_response].lower()})

# write data back
json.dump(data, open(output, 'w'), indent = 2)
