import csv
import re
import os

for filename in [f for f in os.listdir('.') if os.path.isfile(f) and '.csv' in f]:
        print(filename)
        input_string = re.sub('\.csv$', '', filename)

        see_hear = []
        see = []
        hear = []
        neither = []
        with open(filename, 'r', newline = '') as f:
                reader = csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True)
                header = next(reader)
                see_hear.append(header)
                see.append(header)
                hear.append(header)
                neither.append(header)

                for row in reader:
                        if row[35] == '1':
                                see_hear.append(row)
                        elif row[35] == '0':
                                neither.append(row)
                        elif row[35] == '-2':
                                hear.append(row)
                        elif row[35] == '-1':
                                see.append(row)

                csv.writer(open('both/' + input_string + "-see-hear" + ".csv", 'w')).writerows(see_hear)
                csv.writer(open('see/' + input_string + "-see" + ".csv", 'w')).writerows(see)
                csv.writer(open('hear/' + input_string + "-hear" + ".csv", 'w')).writerows(hear)
                csv.writer(open('neither/' + input_string + "-neither" + ".csv", 'w')).writerows(neither)
