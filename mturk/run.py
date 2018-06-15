import sys
import boto3
import csv
import re

# TODO: make these command line arguments
#
# "live"
# "sandbox"
#
# "temporal"
# "spatial"
# "audio"
mturk_type = "sandbox"
data_type = "temporal"
data_path = "data/"
template_path = "templates/"
output_file = "active-hits.txt"

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
        "duration": 3 * 60, # 3 minutes
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

# read command line arguments...
# TODO!

# set the turk environment
mturk_environment = environments[mturk_type]

# set the data environment
data_environment = environments[data_type]

# use profile if one was passed as an arg, otherwise
profile_name = sys.argv[1] if len(sys.argv) >= 2 else None
session = boto3.Session(profile_name = profile_name)
client = session.client(service_name = 'mturk', region_name = 'us-east-1', endpoint_url = mturk_environment['endpoint'])

# print balance
print("Your account balance is {}".format(client.get_account_balance()['AvailableBalance']))

# open csv, create a HIT for each csv line
file_in = open(data_path + data_environment['csv'], "r")
file_out = open(output_file, "w")
reader = csv.reader(file_in)
headers = next(reader)
print("Parameters: " + ', '.join(headers))
# get the question template
template = open(template_path + data_environment['xml'], "r").read()
# go through each row in the csv
for row in reader:
    q = template
    # replace each ${var} with the corresponding row data
    for i, ele in enumerate(headers):
        q = re.sub("\$\{" + ele + "\}", row[i], q)
    # create the HIT
    response = client.create_hit(
        MaxAssignments = data_environment['assignments'],
        LifetimeInSeconds = data_environment['lifetime'],
        AssignmentDurationInSeconds = data_environment['duration'],
        Reward = data_environment['reward'],
        Title = data_environment['title'],
        Keywords = data_environment['keywords'],
        Description = data_environment['desc'],
        Question = q,
        QualificationRequirements = data_environment['worker'],
    )
    # print HIT details
    hit_type_id = response['HIT']['HITTypeId']
    hit_id = response['HIT']['HITId']
    print("Created HIT: {}".format(hit_id))
    print("You can work the HIT here:")
    print(mturk_environment['preview'] + "?groupId={}\n".format(hit_type_id))
    file_out.write("HIT: " + response['HIT']['HITId'] + ", Group: " + response['HIT']['HITTypeId'] + "\n")
print("You can see results here:")
print(mturk_environment['manage'])
file_in.close()
file_out.close()

print("Done.")
