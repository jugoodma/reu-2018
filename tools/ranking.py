from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

url = "https://research.google.com/audioset/dataset/index.html"
page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
output = csv.writer(open("label-rankings.csv", "w", newline = ''), delimiter = ',', quotechar = '"')

table = soup.select_one("table#dataset-index")
output.writerow([th.text for th in table.select("tr th")])
output.writerows([[td.text for td in row.find_all("td")] for row in table.select("tr + tr")])
