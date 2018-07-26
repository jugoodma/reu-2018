import csv
import sys
name = sys.argv[1]

with open(name) as source:
    rdr = csv.reader(source)
    with open ("results") as result:
        wtr = csv.writer(result)
        for r in rdr:
            wtr.writerow( (r[27], r[28], r[29], r[30], r[31]) )