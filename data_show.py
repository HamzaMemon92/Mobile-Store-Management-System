import sqlite3 as sq
import csv
import insert_data
con=sq.connect('mobile.db')
cur=con.cursor()
print("connection done")
def data_show():
    print("Data from supplier Table")
    cur.execute("""select * from Supplier; """)
    for row in cur.fetchall():
        print(row,"\n")
    print("Data from Brand Table")
    cur.execute("""select * from Brand; """)
    for row in cur.fetchall():
        print(row,"\n")
    print("Data from customer Table",)
    cur.execute("""select * from customer; """)
    for row in cur.fetchall():
        print(row,"\n")
    print("Data from purchase Table")
    cur.execute("""select * from purchase; """)
    for row in cur.fetchall():
        print(row,"\n")
    print("Data from Mobile_Stock Table")
    cur.execute("""select * from Mobile_Stock; """)
    for row in cur.fetchall():
        print(row,"\n")
    print("Data from Sales_Bill Table")
    cur.execute("""select * from Sales_Bill; """)
    for row in cur.fetchall():
        print(row,"\n")
    print("Data from Sales_Detail Table")
    cur.execute("""select * from Sales_Details; """)
    for row in cur.fetchall():
        print(row,"\n")





