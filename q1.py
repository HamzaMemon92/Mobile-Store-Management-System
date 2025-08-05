import sqlite3 as sq
import csv
con=sq.connect('mobile.db')
cur=con.cursor()
print("Data from Mobile_Stock Table")
cur.execute("""select * from Mobile_Stock; """)
for row in cur.fetchall():
    print(row,"\n")
