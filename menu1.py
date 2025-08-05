import sqlite3 as sq
def show_menu():
    while True:
        print("\nMenu:")
        print("1. Purchase Stock")
        print("2. Sell Stock")
        print("3. Exit")
        
        choice = input("Enter choice: ")

        if choice == "1":
            purchase_stock()
        elif choice == "2":
            sell_stock()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

def purchase_stock():
    con = sq.connect('mobile.db')
    cur = con.cursor()

    while True:
        # Show available suppliers
        cur.execute("SELECT Supplier_ID, Name FROM Supplier")
        suppliers = cur.fetchall()
        print("\nAvailable Suppliers:")
        for supplier in suppliers:
            print(f"ID: {supplier[0]}, Name: {supplier[1]}")

        supplier_id = input("Select Supplier ID: ")

        # Show phones supplied by this supplier
        cur.execute("""
            SELECT DISTINCT m.Mobile_ID, m.Model, m.Purchase_Price 
            FROM Mobile_Stock m 
            WHERE m.Mobile_ID IN (SELECT Mobile_ID FROM Purchase WHERE Supplier_ID = ?)
        """, (supplier_id,))
        
        mobiles = cur.fetchall()

        print("\nPhones Available from this Supplier:")
        for mobile in mobiles:
            print(f"ID: {mobile[0]}, Model: {mobile[1]}, Purchase Price: {mobile[2]}")

        mobile_id = input("Select Mobile ID to purchase: ")
        quantity = int(input("Enter Quantity: "))

        # Fetch purchase price from database (fixed price)
        cur.execute("SELECT Purchase_Price FROM Mobile_Stock WHERE Mobile_ID = ?", (mobile_id,))
        purchase_price = cur.fetchone()[0]  

        purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")

        # Insert purchase details
        total_amount = quantity * purchase_price
        cur.execute("""
            INSERT INTO Purchase (Supplier_ID, Mobile_ID, Quantity, Purchase_Price, Purchase_Date) 
            VALUES (?, ?, ?, ?, ?)
        """, (supplier_id, mobile_id, quantity, purchase_price, purchase_date))

        # Update stock
        cur.execute("UPDATE Mobile_Stock SET Quantity = Quantity + ? WHERE Mobile_ID = ?", (quantity, mobile_id))
        con.commit()

        print(f"\nPurchase Bill Generated:\nSupplier: {supplier_id}, Mobile ID: {mobile_id}, Quantity: {quantity}, Total Amount: {total_amount}\n")

        # Ask if user wants to buy from another supplier
        more = input("Do you want to buy from another supplier? (yes/no): ")
        if more.lower() != "yes":
            break

def sell_stock():
    con = sq.connect('mobile.db')
    cur = con.cursor()


    # Show available stock
    cur.execute("SELECT * FROM Mobile_Stock WHERE Quantity > 0")
    mobiles = cur.fetchall()

    print("\nAvailable Phones:")
    for mobile in mobiles:
        print(f"ID: {mobile[0]}, Model: {mobile[2]}, Quantity: {mobile[3]}, Selling Price: {mobile[5]}")

    # Get customer details
    name = input("Enter Customer Name: ")
    contact = input("Enter Contact: ")
    address = input("Enter Address: ")
    cur.execute("INSERT INTO Customer (Name, Contact, Address) VALUES (?, ?, ?)", (name, contact, address))
    customer_id = cur.lastrowid  # Get the ID of the inserted customer

    bill_total = 0
    bill_items = []

    while True:
        mobile_id = input("Select Mobile ID to sell: ")
        quantity = int(input("Enter Quantity: "))
        
        # Get Selling Price and Model Name
        cur.execute("SELECT Model, Selling_Price FROM Mobile_Stock WHERE Mobile_ID = ?", (mobile_id,))
        result = cur.fetchone()
        model_name = result[0]
        selling_price = result[1]
        
        total_price = quantity * selling_price
        bill_total += total_price
        bill_items.append((mobile_id, model_name, quantity, selling_price))

        # Reduce Stock
        cur.execute("UPDATE Mobile_Stock SET Quantity = Quantity - ? WHERE Mobile_ID = ?", (quantity, mobile_id))
        
        more = input("Do you want to sell another phone? (yes/no): ")
        if more.lower() != "yes":
            break

    # Insert into Sales_Bill
    cur.execute("INSERT INTO Sales_Bill (Customer_ID, Total_Quantity, Total_Amount) VALUES (?, ?, ?)",
                (customer_id, sum(item[2] for item in bill_items), bill_total))
    bill_id = cur.lastrowid  # Get the Bill ID

    # Insert into Sales_Details
    for item in bill_items:
        cur.execute("INSERT INTO Sales_Details (Bill_ID, Mobile_ID, Quantity, Selling_Price) VALUES (?, ?, ?, ?)",
                    (bill_id, item[0], item[2], item[3]))

    con.commit()

    # *🔹 Display Full Sales Bill*
    print("\n Sales Bill Generated:")
    print(f" Bill ID: {bill_id}")
    print(f" Customer Name: {name}")
    print(f" Contact: {contact}")
    print(f" Address: {address}")
    print(f" Total Amount: ₹{bill_total}\n")
    print(" Purchased Items:")
    
    for item in bill_items:
        print(f"🔹 *Mobile ID:* {item[0]} | *Model:* {item[1]} | *Quantity:* {item[2]} | *Selling Price:* ₹{item[3]}")

show_menu()
