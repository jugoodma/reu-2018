import sqlite3
import csv
import itertools
import re

try:
    # begin
    name = 'test.db' # change this if you want a NEW database. make sure this name matches in app.py
    interval = 0.5
    window = 1.0
    labels_file = 'class_labels_indices.csv'
    data_file = 'unbalanced_train_segments.csv'
    start_row = 3
    stop_row = 103
    labels = {}
    conn = sqlite3.connect('data/' + name)
    c = conn.cursor()
    print('Creating database ' + name + ' with ' + str(interval) + 'sec intervals and ' + str(window) + 'sec window. Version: ' + sqlite3.version)
    # create dictionary for mapping obscured labels to human-readable labels
    with open(labels_file, newline = '') as f:
        reader = csv.reader(f)
        next(reader) # skip the first line since it has headers for the columns
        for row in reader:
            labels[row[1]] = row[2]
    # create Audioset table
    c.execute('CREATE TABLE Audioset_Video(YTID VARCHAR(16) NOT NULL, label VARCHAR(64), PRIMARY KEY (YTID))')
    # read data in specified range
    with open(data_file, newline = '') as f:
        reader = itertools.islice(csv.reader(f, quotechar = '"', delimiter = ',', quoting = csv.QUOTE_ALL, skipinitialspace = True), start_row, stop_row)
        for row in reader:
            lbls = ', '.join(list(map(lambda l: labels[l],row[3].split(','))))
            ytid = re.search('^(=?)(.*)$', row[0]).group(2)
            c.execute('INSERT INTO Audioset_Video VALUES (?,?)', (ytid, lbls))
            # create Clip table
    # end
    conn.commit()
    conn.close()
    print('Done.')
except sqlite3.Error as e:
    print(e)
