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
prog = re.compile("^HIT: (.*), Group: (.*)$")
def check(line):
    result = False
    print(line)
    hit_id = prog.match(line).group(1)
    print(client.list_assignments_for_hit(HITId = hit_id, AssignmentStatuses = ['Submitted', 'Approved'], MaxResults=10,))
    return result

# open active hits file and check each line for completed hits
# run each line through the checker
# only save lines which return false
current = [x for x in open(output_file, "r").read().splitlines() if not check(x)]

# re-write output_file
open(output_file, "w").write('\n'.join(current))

print("Done.")
