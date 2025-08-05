import sqlite3 as sq
import csv

def insert_data():
    con = sq.connect('mobile.db')
    cur = con.cursor()

    # Insert supplier data
    with open('supplier.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute("INSERT INTO Supplier (Name, Contact, Address) VALUES (?, ?, ?)", row)
    print("Data inserted into table supplier")

    #  Insert brand data
    with open('brand.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute("INSERT INTO Brand (Brand_Name) VALUES (?)", row)
    print("Data inserted into table Brand")

    #  Insert customer data
    with open('customer.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute("INSERT INTO Customer (Name, Contact, Address) VALUES (?, ?, ?)", row)
    print("Data inserted into table customer")

    #  Insert mobile stock data
    with open('mobilestock.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute("""
                INSERT INTO Mobile_Stock (Brand_ID, Model, Quantity, Purchase_Price, Selling_Price, Supplier_ID)
                VALUES (?, ?, ?, ?, ?, ?)
            """, row)
    print("Data inserted into table mobilestock")

    #  Insert purchase data
    with open('purchase.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute("""
                INSERT INTO Purchase (Supplier_ID, Mobile_ID, Quantity, Purchase_Price, Purchase_Date)
                VALUES (?, ?, ?, ?, ?)
            """, row)
    print("Data inserted into table purchase")

    con.commit()
    con.close()
