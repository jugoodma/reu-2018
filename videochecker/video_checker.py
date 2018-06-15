import requests
from pprint import pprint
import csv
import json


"""
with open('/home/marc/Desktop/reu-2018/msr_csv.csv', 'r') as msr:
    read = csv.reader(msr)
    for row in read:
        print(row[0])


url = 'https://www.googleapis.com/youtube/v3/videos?id=AZZME-uNC0I&key=AIzaSyAZUmdgun5Ao9D2kz43MxrCGOKkqsYsfFU&part=status'
url_get = requests.get(url)
print(url_get.json())
"""

with open('/home/marc/Desktop/reu-2018/msr_csv.csv', 'r') as msr:
    read = csv.reader(msr)
    for row in read:
        ytid = row[0]
        url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=AIzaSyAZUmdgun5Ao9D2kz43MxrCGOKkqsYsfFU&part=status' % ytid
        url_get = requests.get(url)
        #print(url_get.json())

        if len(url_get.json()['items']) == 0:
            print("not available: ", ytid, "\n")
            



 
