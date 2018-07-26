import csv
import itertools
import re
import json
import math
import requests
from settings import *
import sys




#input_file = sys.argv[1]

for file_name in os.listdir('.'):
    input_file = file_name

    input_string = re.sub('\.csv$', '', input_file)

    reader = csv.reader(open(input_file, 'r', newline = ''), quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    writer_see_hear = open(input_string + " SEE HEAR" + ".csv", "w+")
    writer_see = open(input_string + " SEE" + ".csv", "w+")
    writer_hear = open(input_string + " HEAR" + ".csv", "w+")
    writer_neither = open(input_string + " NEITHER" + ".csv", "w+")
    csv_writer_see_hear = csv.writer(writer_see_hear)
    csv_writer_see = csv.writer(writer_see)
    csv_writer_hear = csv.writer(writer_hear)
    csv_writer_neither = csv.writer(writer_neither)


    header = next(reader)

    csv_writer_see_hear.writerow(header)
    csv_writer_see.writerow(header)
    csv_writer_hear.writerow(header)
    csv_writer_neither.writerow(header)

    for row in reader:
        if row[35] == '1':
            csv_writer_see_hear.writerow(row)
        elif row[35] == '0':
            csv_writer_neither.writerow(row)
        elif row[35] == '-2':
            csv_writer_hear.writerow(row)
        elif row[35] == '-1':
            csv_writer_see.writerow(row)
        