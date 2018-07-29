# miscelaneous tool for us to use
# checks each row in an input .csv file and removes youtube videos that do not exist

import sys
import csv
from settings import *

temp = []
p = ""
if len(sys.argv) < 2:
    p = input("file name: ")
else:
    p = sys.argv[1]
with open(input_path + p) as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    temp.append(next(reader))
    for row in reader:
        if youtube_video_exists(row[0]):
            temp.append(row)
        else:
            print(row)
with open(input_path + p, 'w') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    writer.writerows(temp)
