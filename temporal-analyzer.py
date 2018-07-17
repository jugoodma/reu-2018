import csv
import itertools
import re
import json
import math
import requests
from settings import *
import random
# begin


input_data = 'Batch_3281353_batch_results.csv'

output_data = 'results/temporal-analyzed.csv'

response_data = 'amazon_batch_response.csv'

#reject_list = open('temporal_analyzed_rejects.csv', 'w', newline = '')


writer_response = csv.writer(open(response_data, 'w', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
reader_writer = csv.reader(open(input_data, 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
writer = csv.writer(open(output_data, 'w', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
#ytid = row[27], start = row[28], end = row[29], label = row[30], contains = row[32], values = row[36]-row[45], QA = row[46], approve = row[48], reject = row[49]

# create csv file with clips


# write the header row
#writer.writerow(['ytid'] + ['start'] + ['end'] + ['labels'] + ['seconds'])
 # + ['second_2'] + ['second_3'] + ['second_4'] + ['second_5'] + ['second_6'] + ['second_7'] + ['second_8'] + ['second_1'] + ['second_1']
# read data in specified range



with open(input_data, 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    next(reader)
    for row in reader:
        
        #ytid = row[27], start = row[28], end = row[29], label = row[30], contains = row[32], values = row[36]-row[45], QA = row[46], approve = row[48], reject = row[49]

        if row[46] == '0':
            writer_response.writerow(row+['']+['Did not play the video'])
            continue
        else:
            writer_response.writerow(row+ ['x'] + [''])

            response_list = []

            x = 36
            if row[x]:
                response_list.append(row[x])
                x += 1
                
            #response_list = [int(row[36]), int(row[37]), int(row[38]), int(row[39]), int(row[40]), int(row[41]), int(row[42]), int(row[43]), int(row[44]), int(row[45])]    
            if filter(lambda s: (sum(s) > 0), response_list):
                writer.writerow([row[27], row[28], row[29], response_list])


    

# end
print('Done.')
