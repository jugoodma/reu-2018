import sqlite3
import csv

name = "test.db" # change this if you want a NEW database
interval = 0.5
window = 1.0
csv_file = "unbalanced_train_segments.csv"

try:
    conn = sqlite3.connect("data/" + name)
    print("Creating database " + name + " with " + str(interval) + "sec intervals and " + str(window) + "sec window. Version: " + sqlite3.version)

    

    print("Done.")
    conn.close()
except sqlite3.Error as e:
    print(e)
