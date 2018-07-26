# DEFAULT SETTINGS FILE
import json
import requests

mturk_type = "sandbox"
data_type = "temporal"
data_path = "../data/"
input_path = "../input/"
template_path = "../templates/"
result_path = "../results/"
max_results = 10
approve_all = False

# you must have a YouTube API v3 key
# your key must be in a json file titled:
#   'youtube-key.json'
# with structure:
#  {
#    "key": "<YOUR API KEY HERE>"
#  }
# obviously without the <>
#
# our .gitignore ignores json files so your
# key will not be public
youtube_api = 'https://www.googleapis.com/youtube/v3/videos?id={}&key=' + json.loads(open('../youtube-key.json', 'r').read())['key'] + '&part=status'

# if the items list is > 0 then the youtube video exists/is watchable
def youtube_video_exists(ytid):
    return len(requests.get(youtube_api.format(ytid)).json()['items']) > 0

# environments variable includes both mturk and data environments
# mturk - live, sandbox
# data - temporal, spatial, audio
#
# It's best not to edit the mturk environments
#
# DATA ENVIRON:
# assignments - number of unique workers per HIT
# lifetime    - number of seconds that each HIT is visible
# duration    - number of seconds that the assignment is available to the worker
# approve     - number of seconds after assignment is submitted that it is auto-approved
# reward      - cost per assignment
# title       - the title of the HIT
# keywords    - the keywords of the HIT
# desc        - the description of the HIT
# xml         - the xml file for this HIT
# worker      - requirements for the HIT worker
#   go to http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs
#   to read the worker requirements. you may want to use masters only for certain data collection environments
environments = {
    # mturk environ.
    "live": {
        "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
        "preview": "https://www.mturk.com/mturk/preview",
        "manage": "https://requester.mturk.com/mturk/manageHITs",
    },
    "sandbox": {
        "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
        "preview": "https://workersandbox.mturk.com/mturk/preview",
        "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
    },
    # data environ.
    "temporal": {
        "csv": "temporal-input.csv",
        "assignments": 1,
        "lifetime": 3 * 24 * 60 * 60, # 3 days
        "duration": 10 * 60, # 10 minutes
        "approve": 5 * 24 * 60 * 60, # 5 days
        "reward": "0.07",
        "title": "Annotate when audio source appears in video",
        "keywords": "annotating, video, audio",
        "desc": "Watch a 10 second video clip and tell us when the source of a labeled sound appears in the frame of the video",
        "xml": "temporal-ui.xml",
        "worker": [{
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [95],
            'RequiredToPreview': True,
        }],
        "hit-type-id": "3ISL4H6O6ITRSQNC3OSL4OKOO05ICC",
        "out": "temporal-output.csv",
    },
    "spatial": {
        "csv": "spatial-input.csv",
        "assignments": 1,
        "lifetime": 3 * 24 * 60 * 60, # 3 days
        "duration": 5 * 60, # 5 minutes
        "approve": 3 * 24 * 60 * 60, # 3 days
        "reward": "0.02",
        "title": "Locate Where Audio Originates in a Video",
        "keywords": "matching, video, audio",
        "desc": "Watch a 1 second video clip and indicate where the audio is coming from",
        "xml": "spatial-ui.xml",
        "worker": [{
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [80],
            'RequiredToPreview': True,
        }],
        "hit-type-id": "3M8DJV5FJWDQ93IDR6VEH2187CRFN0",
        "out":"spatial-output.csv",
    },
    # this is out-dated
    "captions": {
        "csv": "captions-input.csv",
        "assignments": 2,
        "lifetime": 7 * 24 * 60 * 60, # 7 days
        "duration": 60 * 60, # 1 hour
        "approve": 5 * 24 * 60 * 60, # 5 days
        "reward": "0.07",
        "title": "Annotate a video without visual context",
        "keywords": "classify, video, audio",
        "desc": "Listen to a blurred 10 to 30 second video and describe what happens in the audio scene",
        "xml": "audio-ui.xml",
        "worker": [{
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [95],
            'RequiredToPreview': True,
        }],
        "hit-type-id": "",
        "out":"audio-output.csv",
    },
}
