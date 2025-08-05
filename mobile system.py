import sqlite3 as sq
import insert_data
import data_show

# Connect to the database
con = sq.connect('mobile.db')
cur = con.cursor()
print(" Connection successful")

# Dictionary of all table creation queries
tables = {
    "Supplier_Table": """
    CREATE TABLE IF NOT EXISTS Supplier (  
        Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Name VARCHAR(100) NOT NULL,  
        Contact VARCHAR(15) UNIQUE NOT NULL,  
        Address VARCHAR(50) NOT NULL  
    );
    """,

    "Brand_Table": """
    CREATE TABLE IF NOT EXISTS Brand (  
        Brand_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Brand_Name VARCHAR(50) UNIQUE NOT NULL  
    );
    """,

    "Mobile_Stock_Table": """
    CREATE TABLE IF NOT EXISTS Mobile_Stock (  
        Mobile_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Brand_ID INTEGER,  
        Model VARCHAR(100) UNIQUE NOT NULL,  
        Quantity INTEGER NOT NULL DEFAULT 0,  
        Purchase_Price DECIMAL(10,2) NOT NULL,  
        Selling_Price DECIMAL(10,2) NOT NULL,  
        Supplier_ID INTEGER,  
        FOREIGN KEY (Brand_ID) REFERENCES Brand(Brand_ID)  
            ON DELETE CASCADE ON UPDATE CASCADE,  
        FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID)  
            ON DELETE SET NULL ON UPDATE CASCADE  
    );
    """,

    "Customer_Table": """
    CREATE TABLE IF NOT EXISTS Customer (  
        Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Name VARCHAR(100) NOT NULL,  
        Contact VARCHAR(15) UNIQUE NOT NULL,  
        Address VARCHAR(50)
    );
    """,

    "Purchase_Table": """
    CREATE TABLE IF NOT EXISTS Purchase (  
        Purchase_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Supplier_ID INTEGER,  
        Mobile_ID INTEGER,  
        Quantity INTEGER NOT NULL,  
        Purchase_Price DECIMAL(10,2) NOT NULL,  
        Total_Amount DECIMAL(10,2) GENERATED ALWAYS AS (Quantity * Purchase_Price) STORED,  
        Purchase_Date DATE NOT NULL,  
        FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID)  
            ON DELETE CASCADE ON UPDATE CASCADE,  
        FOREIGN KEY (Mobile_ID) REFERENCES Mobile_Stock(Mobile_ID)  
            ON DELETE CASCADE ON UPDATE CASCADE  
    );
    """,

    "Sales_Bill_Table": """
    CREATE TABLE IF NOT EXISTS Sales_Bill (  
        Bill_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Customer_ID INTEGER,  
        Total_Quantity INTEGER DEFAULT 0 ,  
        Total_Amount DECIMAL(10,2) DEFAULT 0.00,  
        Sale_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)  
            ON DELETE CASCADE ON UPDATE CASCADE  
    );
    """,

    "Sales_Details_Table": """
    CREATE TABLE IF NOT EXISTS Sales_Details (  
        Sale_ID INTEGER PRIMARY KEY AUTOINCREMENT,  
        Bill_ID INTEGER,  
        Mobile_ID INTEGER,  
        Quantity INTEGER NOT NULL,  
        Selling_Price DECIMAL(10,2) NOT NULL,  
        FOREIGN KEY (Bill_ID) REFERENCES Sales_Bill(Bill_ID)  
            ON DELETE CASCADE ON UPDATE CASCADE,  
        FOREIGN KEY (Mobile_ID) REFERENCES Mobile_Stock(Mobile_ID)  
            ON DELETE CASCADE ON UPDATE CASCADE  
    );
    """
}

# Create each table
for table_name, table_query in tables.items():
    cur.execute(table_query)
    print(f"✅ Table '{table_name}' created successfully.")

# Create triggers
trigger_queries = [

    # Update Sales_Bill after new sale
    """
    CREATE TRIGGER IF NOT EXISTS Update_SalesBill_Total
    AFTER INSERT ON Sales_Details
    FOR EACH ROW
    BEGIN
        UPDATE Sales_Bill  
        SET 
            Total_Amount = (
                SELECT SUM(Quantity * Selling_Price)  
                FROM Sales_Details  
                WHERE Bill_ID = NEW.Bill_ID  
            ),
            Total_Quantity = (
                SELECT SUM(Quantity)  
                FROM Sales_Details  
                WHERE Bill_ID = NEW.Bill_ID  
            )
        WHERE Bill_ID = NEW.Bill_ID;
    END;
    """,

    # Reduce mobile stock after sale
    """
    CREATE TRIGGER IF NOT EXISTS Update_MobileStock_After_Sale
    AFTER INSERT ON Sales_Details
    FOR EACH ROW
    BEGIN
        UPDATE Mobile_Stock
        SET Quantity = Quantity - NEW.Quantity
        WHERE Mobile_ID = NEW.Mobile_ID;
    END;
    """,

    # Increase stock after purchase
    """
    CREATE TRIGGER IF NOT EXISTS Update_MobileStock_After_Purchase
    AFTER INSERT ON Purchase
    FOR EACH ROW
    BEGIN
        UPDATE Mobile_Stock
        SET Quantity = Quantity + NEW.Quantity
        WHERE Mobile_ID = NEW.Mobile_ID;
    END;
    """
]

# Execute triggers
for trigger in trigger_queries:
    cur.executescript(trigger)

# Commit changes
con.commit()

# Insert demo data
insert_data.insert_data()
print(" All tables created and data inserted successfully.")

# Display data
data_show.data_show()
print(" All data displayed successfully.")

# Close connection
con.close()
