import csv
import json
from datetime import datetime
from settings import *

input_data = input("What file would you like to run: ./results/")
dt = input("Which data type is this file? (audio or video): ")

desc = "change me"
today = str(datetime.now())

output = "audio-video-dataset.json"
data = json.load(open(output, 'r'))
msrvtt = json.load(open(data_path + "videodatainfo_2017.json", 'r'))
r = 50 # number of sentences per video (actual value is 2, but we padded this in case we add to the dataset)

data['info']['description'] = desc
data['info']['data_created'] = today

# audio:
# Audio (blacked out video)
# 

# video:
# Video (muted audio)
# 

# create video key-val lookup
vids = {}
for obj in msrvtt['videos']:
    ytid = obj['url'].split('=')[1]
    obj.pop('url')
    obj['ytid'] = ytid
    obj['origin'] = 'msrvtt'
    vids[ytid, obj['start time']] = obj

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
        elif ele == "AutoApprovalTime": # "ApprovalTime"
            idx_approval = idx
        else:
            continue

    # use these indices to append to the data
    for row in reader:
        # we only want approved data
        if not row[idx_approval] == "":
            # get msrvtt video entry
            v = vids[row[idx_ytid], float(row[idx_start])]
            # get data entry
            i = -1
            for idx, obj in enumerate(data['data']):
                if obj['id'] <= v['id']:
                    i = idx
            if i == -1 or not data['data'][i]['id'] == v['id']:
                # data not found, insert new data after this index
                #   or
                # no data, this is the first run
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
json.dump(data, open(output, 'w'))
