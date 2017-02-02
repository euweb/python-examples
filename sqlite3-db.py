#!/usr/bin/env python

import time
import sqlite3
from datetime import datetime

counter = None

def main():    

    proc = DBProcessor()
    proc.setup()

    proc.print_db()

    counter = proc.get_current_max()
    if counter is None:
        counter = 0.0

    counter += 0.01

    proc.update(counter,format(str(datetime.now())),1)
    done = False
    while not done:

        try:

            counter += 0.01
            proc.update(counter,format(str(datetime.now())),0)
            time.sleep(1)

        except KeyboardInterrupt:
            done = True


class DBProcessor:        

    #db configuration
    DB = "gasmeter.db"

    _conn = None

    def __init__(self):
        pass

    def __del__(self):
        if self._conn is not None:
            self._conn.close()

    def setup(self):
        # create db if needed
        self._conn = sqlite3.connect(self.DB)
        self._conn.isolation_level = None # -> autocommit
        self._conn.execute("""
        CREATE TABLE IF NOT EXISTS gas_meter(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          date DATETIME NOT NULL,
          value REAL NOT NULL,
          type INTEGER
        );
        """)

    def get_current_max(self):
     
        cursor = self._conn.cursor()

        # preselect counter value
        current = cursor.execute("SELECT value FROM gas_meter ORDER BY id DESC LIMIT 1;")
        cur_counter = current.fetchone()
        counter = None
        if cur_counter is not None:
            print "loading current counter value from database: ",cur_counter[0]
            counter = float(cur_counter[0])

        cursor.close()
        return counter


    def update(self, counter, time, type):
        print "counter: ",counter,", type: ",type
        cursor = self._conn.cursor()
        cursor.execute("insert into gas_meter (id, date, value, type) values (null,?,?,?)",(time,counter,type))
        cursor.close()


    def print_db(self):
        cursor = self._conn.cursor()
        # show contents of the TABLE
        cursor.execute("select * from gas_meter;")
        result = cursor.fetchall()
        for r in result:
            print(r)
        cursor.close()

if __name__ == "__main__":
    main()


