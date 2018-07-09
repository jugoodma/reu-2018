# this file generates the estimated quality rankings of each label given in google audioset
# then it parses ontology.json and removes each label with children

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import json

soup = BeautifulSoup(urlopen("https://research.google.com/audioset/dataset/index.html"), "html.parser")
output = csv.writer(open("label-rankings-no-child.csv", "w", newline=""), delimiter = ',', quotechar = '"')
ontology = open("data/ontology.json", 'r', encoding='latin-1')
temp = []

table = soup.select_one("table#dataset-index")
header = [th.text for th in table.select("tr th")]
for row in table.select("tr + tr"):
    temp.append([td.text for td in row.find_all("td")])

for obj in json.load(ontology):
    if len(obj['child_ids']) > 0:
        temp = [x for x in temp if not obj['name'] in x]

output.writerow(header)
output.writerows(temp)
