import sqlite3


conn = sqlite3.connect('data/test.db') #creating a connection objection to represent the database
c = conn.cursor() # a cursor object used to execute SQL commands
c.execute("""SELECT YTID, label FROM Audioset_Video""")
ytid = c.fetchone()[0]
temp_label = c.fetchone()[1]
symbol = ytid

c.execute("""SELECT start, end FROM '%s' WHERE '%s'.sent = "0" """ % (symbol, symbol))
temp_row = c.fetchone()
temp_start = temp_row[0]
temp_end = temp_row[1]

data_return = '{"id":"' + str(ytid) + '","start":' + str(temp_start) + ',"end":' + str(temp_end) + ',"labels":"' + temp_label + '"}'
print (data_return)
#'{"id":"M7lc1UVf-VE","start":0.0,"end":10.0,"labels":"some, labels, here"}'
c.execute("""UPDATE '%s' SET sent = "1" """ % symbol)
