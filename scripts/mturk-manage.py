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

# gets text in xml node
def getText(nodelist):
    return " ".join(t.nodeValue for t in nodelist if t.nodeType == t.TEXT_NODE)

# parse function
def parse(answer):
    result = None
    answer_xml = parseString(answer)
    identifier = None
    i = 0
    ans = answer_xml.getElementsByTagName('Answer')
    while i < len(ans) and not identifier:
        if getText(ans[i].getElementsByTagName('QuestionIdentifier')[0].childNodes) == 'identifier':
            identifier = getText(ans[i].getElementsByTagName('FreeText')[0].childNodes)
        i += 1
    if identifer == 'temporal' or identifier == 'audio':
        # temporal parse
        # audio parse (same parsing)
        qa = None
        response = None
        ytid = None
        tp = "Temporal" if identifier == 'temporal' else "Audio"
        i = 0
        while i < len(ans):
            qi = getText(ans[i].getElementsByTagName('QuestionIdentifier')[0].childNodes)
            ft = getText(ans[i].getElementsByTagName('FreeText')[0].childNodes)
            if qi == 'qa':
                qa = ft
            elif qi == 'response':
                response = ft
            elif qi == 'ytid':
                ytid == ft
            i += 1
        result = {"type":identifier, "pretty":tp + " - QA: " + qa + ", Response: " + response, "row":[ytid] + [qa] + [response]}
    elif identifier == 'spatial':
        # TODO: this!!
        # spatial parse
        qa = None
        '''
        res_matrix = []
        for j in range(18):
            res_matrix.append([])
        prog = re.compile("loc\-(.*)")
        i = 0
        while i < len(ans):
            qi = getText(ans[i].getElementsByTagName('QuestionIdentifier')[0].childNodes)
            ft = getText(ans[i].getElementsByTagName('FreeText')[0].childNodes)
            if qi == 'qa':
                qa = ft
            elif qi.contains("loc-"):
                
            i += 1
        result = "Spatial - QA: " + qa + ", Response Matrix:\n" + "\n".join(res_matrix)
        '''
        result = {"type":"spatial", "pretty":"Spatial - xml: " + answer, "row":[]}
    else:
        # unknown identifier
        result = {"type":"unknown", "pretty":"Unknown type, raw xml: " + answer, "row":[]}
    return result

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
                p = parse(assignment['Answer'])
                print(p['pretty'])
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
                if p['type'] != 'unknown':
                    csv.writer(open(data_path + environments[p['type']], 'a')).writerow([hit['HITId']] + p['row'])
            print("Next...")
    hit_list = client.list_hits(MaxResults = max_results, NextToken = next_token)
    num_results = hit_list['NumResults']

print("Done.")
