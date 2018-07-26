# comments about this file
# 

import csv

spatial = input("filename: ./")
approve = input("approval file: ./")
reject = input("reject file: ./")
default = "We are sorry to reject your HIT but it is of poor quality." # default rejection message

# HIT IDs that are approved
a = []
with open(approve, 'r', newline = '') as f:
    reader = csv.reader(f, delimiter = ',', quotechar = '"')
    for row in reader:
        a.append(row[0])

# HIT IDs that are rejected
rej = {}
r = [] # slim version of above list
with open(reject, 'r', newline = '') as f:
    reader = csv.reader(f, delimiter = ',', quotechar = '"')
    for row in reader:
        rej[row[0]] = row[2]
        r.append(row[0])

# get the original MTurk .csv data
header = []
orig = []
with open(spatial, 'r', newline = '') as f:
    reader = csv.reader(f, delimiter = ',', quotechar = '"')
    # get header and collect all indices that matter
    header = next(reader)
    idx_assid = -1 # assignment ID
    idx_approve = -1
    idx_reject = -1
    for idx, h in enumerate(header):
        if h == 'AssignmentId':
            idx_assid = idx
        elif h == 'Approve':
            idx_approve = idx
        elif h == 'Reject':
            idx_reject = idx
        else:
            continue
    # fill in approve/reject for each row in .csv
    for row in reader:
        if row[idx_assid] in a:
            row.append('x')
        elif row[idx_assid] in r:
            message = rej[row[idx_assid]]
            if message is None:
                message = default
            row.append('')
            row.append(message)
        # else do nothing ...
        orig.append(row)

# write output csv for upload
with open(spatial.split(".")[0] + "-upload.csv", 'w', newline = '') as f:
    writer = csv.writer(f, delimiter = ',', quotechar = '"')
    writer.writerow(header)
    writer.writerows(orig)
