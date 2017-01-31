#!/usr/bin/env python

import time
import sqlite3
from datetime import datetime

#db configuration
DB = "gasmeter.db"

# current counter value of gas meter
counter = 0.0

# create db if needed
conn = sqlite3.connect(DB)
conn.execute("""
CREATE TABLE IF NOT EXISTS gas_meter(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATETIME NOT NULL,
  value REAL NOT NULL,
  special INTEGER
);
""")

conn.commit()
conn.close()

# new connecton
conn = sqlite3.connect(DB)
conn.isolation_level = None # -> autocommit

cursor = conn.cursor()

# show contents of the TABLE
cursor.execute("select * from gas_meter;")
result = cursor.fetchall()
for r in result:
    print(r)

# preselect counter value
current = cursor.execute("SELECT value FROM gas_meter ORDER BY id DESC LIMIT 1;")
cur_counter = current.fetchone()

if cur_counter is not None:
    print "loading current counter value from database"
    counter = float(cur_counter[0])
print "counter:",counter

sql_statement = "insert into gas_meter (id, date, value, special) values (null,?,?,?)"

# insert the first row
counter += 0.01
cursor.execute(sql_statement,(format(str(datetime.now())),counter,1))
print "insert first row for counter: ",str(counter)

done = False
while not done:

    try:

        counter += 0.01
        cursor.execute(sql_statement,(format(str(datetime.now())),counter,''))
        print "insert row for counter: ",str(counter)
        time.sleep(1)

    except KeyboardInterrupt:
        cursor.close()
        conn.commit()
        conn.close()
        done = True