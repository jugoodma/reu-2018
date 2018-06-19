import csv

msr = open('msr_csv.csv', 'r')

number_of_videos_per_category = 
sampled = open('msr_csv_sampled.csv', 'w')

csvreader = csv.reader(msr, delimiter = ",")

csvwriter = csv.writer(sampled)

top_list =[[]]

for i in range(19):
    x = []
    top_list.append(x)
bottom_list = []


next(csvreader)
for row in csvreader:
    bottom_list = (row[0], row[1], row[2])
    print(int(row[3]))
    top_list[int(row[3])].append(bottom_list)
    


