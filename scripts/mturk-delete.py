import sys
import boto3
import re
from xml.dom.minidom import parseString
import csv
from settings import *

mturk_environment = environments[mturk_type]

# users can pass in a profile as system argument
profile_name = sys.argv[1] if len(sys.argv) >= 2 else None
session = boto3.Session(profile_name = profile_name)
client = session.client(service_name = 'mturk', region_name = 'us-east-1', endpoint_url = mturk_environment['endpoint'],)

# print account balance
print("Your account balance is {}".format(client.get_account_balance()['AvailableBalance']))

yes = input("THIS WILL DELETE ALL ACTIVE HITS, ARE YOU SURE YOU WANT TO DO THIS?? (yes) ")

if yes == 'yes':
    hit_list = client.list_hits(MaxResults = 100)
    num_results = hit_list['NumResults']
    while num_results > 0:
        for hit in hit_list['HITs']:
            try:
                print("Deleting " + hit['HITId'])
                client.update_expiration_for_hit(HITId = hit['HITId'], ExpireAt = 0)
                client.delete_hit(HITId = hit['HITId'])
            except:
                pass
        hit_list = client.list_hits(MaxResults = 100)
        num_results = hit_list['NumResults']

print("Done.")
