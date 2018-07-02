import csv
from settings import *

temp = []
p = input("file name: ")
with open(data_path + p) as f:
    reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    temp.append(next(reader))
    for row in reader:
        if youtube_video_exists(row[0]):
            temp.append(row)
        else:
            print(row)
with open(data_path + p, 'w') as f:
    writer = csv.writer(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
    writer.writerows(temp)
