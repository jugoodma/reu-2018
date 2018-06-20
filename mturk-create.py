import sys
import boto3
import csv
import re
from settings import *

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
reader = csv.reader(file_in)
headers = next(reader)
print("Parameters: " + ', '.join(headers))
# get the question template
template = open(template_path + data_environment['xml'], "r").read()
# go through each row in the csv
for row in reader:
    q = template
    exist_flag = None
    # replace each ${var} with the corresponding row data
    for i, ele in enumerate(headers):
        if headers[i] == 'ytid' and not youtube_video_exists(row[i]):
            exist_flag = row[i]
        q = re.sub("\$\{" + ele + "\}", row[i], q)
    # create the HIT
    if not exist_flag:
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
    else:
        print("YouTube video " + exist_flag + " does not exist")
print("You can (apparently) see results here:")
print(mturk_environment['manage'])
file_in.close()

print("Done.")
