import sys
import boto3
import re
from xml.dom.minidom import parseString
from settings import *

mturk_environment = environments[mturk_type]

# users can pass in a profile as system argument
profile_name = sys.argv[1] if len(sys.argv) >= 2 else None
session = boto3.Session(profile_name = profile_name)
client = session.client(service_name = 'mturk', region_name = 'us-east-1', endpoint_url = mturk_environment['endpoint'],)

# print account balance
print("Your account balance is {}".format(client.get_account_balance()['AvailableBalance']))

# check a line for the hit and see if hit is completed
# if the hit is not completed, return False
# if the hit is completed, ask the user if we are approving the hit
#   if approved, return True
#   else return False
#
# loop through active hits
print("Beginning HIT manager. Press ENTER to ACCEPT the work with no feedback, 'deny' to DENY the work, 'skip' to SKIP the work, and any thing else will be ACCEPTed and interpreted as feedback ")
hit_list = client.list_hits(MaxResults = max_results)
num_results = hit_list['NumResults']
while num_results > 0:
    next_token = hit_list['NextToken']
    for hit in hit_list['HITs']:
        assignments = client.list_assignments_for_hit(HITId = hit['HITId'])['Assignments']
        for assignment in assignments:
            if assignment['AssignmentStatus'] == 'Submitted':
                print("Assignment ID: " + assignment['AssignmentId'])
                print("Answer:")
                print(assignment['Answer'])
                if approve_all:
                    client.approve_assignment(AssignmentId = assignment['AssignmentId'])
                else:
                    res = input("Do you accept the worker's work? ")
                    if res == 'deny':
                        feed = input("Feedback required for denying: ")
                        client.reject_assignment(AssignmentId = assignment['AssignmentId'], RequesterFeedback = feed)
                    elif res == '':
                        client.approve_assignment(AssignmentId = assignment['AssignmentId'])
                    elif res != 'skip':
                        client.approve_assignment(AssignmentId = assignment['AssignmentId'], RequesterFeedback = res)
            print("Next...")
    hit_list = client.list_hits(MaxResults = max_results, NextToken = next_token)
    num_results = hit_list['NumResults']

print("Done.")
