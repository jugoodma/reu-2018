# DEFAULT SETTINGS FILE
import json
import requests

mturk_type = "sandbox"
data_type = "temporal"
data_path = "data/"
template_path = "templates/"
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
youtube_api = 'https://www.googleapis.com/youtube/v3/videos?id={}&key=' + json.loads(open('youtube-key.json', 'r').read())['key'] + '&part=status'

# if the items list is > 0 then the youtube video exists/is watchable
def youtube_video_exists(ytid):
    return requests.get(youtube_api.format(ytid)).json()['items'] > 0

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
        "reward": "0.01",
        "title": "Determine if Audio Matches Video",
        "keywords": "matching, video, audio",
        "desc": "Watch a 1 second video clip and tell us whether the audio matches what you see in the clip",
        "xml": "temporal-ui.xml",
        "worker": [{
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [80],
            'RequiredToPreview': True,
        }],
        "hit-type-id": "3ISL4H6O6ITRSQNC3OSL4OKOO05ICC",
    },
    "spatial": {
        "csv": "spatial-input.csv",
        "assignments": 1,
        "lifetime": 3 * 24 * 60 * 60, # 3 days
        "duration": 5 * 60, # 5 minutes
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
    },
    "audio": {
        "csv": "audio-input.csv",
        "assignments": 2,
        "lifetime": 3 * 24 * 60 * 60, # 3 days
        "duration": 20 * 60, # 20 minutes
        "reward": "0.10",
        "title": "",
        "keywords": "",
        "desc": "",
        "xml": "audio-ui.xml",
        "worker": [{
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [80],
            'RequiredToPreview': True,
        }],
        "hit-type-id": "",
    },
}
