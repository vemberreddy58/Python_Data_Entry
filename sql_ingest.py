import pyodbc
import random
from datetime import datetime, timedelta
from faker import Faker

# -------------------------------------------
# 1️⃣ Database Connection
# -------------------------------------------
server = 'QHYDL2603'         # e.g., 'LAPTOP123\\SQLEXPRESS' or 'localhost'
database = 'RetailDW'
username = ''          # leave blank if using Windows Authentication
password = ''

# For Windows Authentication:
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# For SQL Authentication:
#connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

fake = Faker()

# -------------------------------------------
# 2️⃣ Insert Customers
# -------------------------------------------
print("Inserting customers...")
for _ in range(50):
    name = fake.name()
    email = fake.email()
    region = random.choice(["North", "South", "East", "West"])
    signup_date = fake.date_between(start_date='-2y', end_date='today')

    cursor.execute("""
        INSERT INTO stg.Customers (CustomerName, Email, Region, SignupDate)
        VALUES (?, ?, ?, ?)
    """, (name, email, region, signup_date))

conn.commit()

# -------------------------------------------
# 3️⃣ Insert Products
# -------------------------------------------
print("Inserting products...")
products = [
    ("Laptop", "Electronics", "Computers", 500, 750),
    ("Headphones", "Electronics", "Accessories", 30, 50),
    ("Smartphone", "Electronics", "Mobiles", 400, 650),
    ("Desk Chair", "Furniture", "Office", 80, 120),
    ("Notebook", "Stationery", "Office", 2, 5),
    ("Coffee Machine", "Appliances", "Kitchen", 90, 150)
]

for prod in products:
    cursor.execute("""
        INSERT INTO stg.Products (ProductName, Category, SubCategory, Cost, Price)
        VALUES (?, ?, ?, ?, ?)
    """, prod)

conn.commit()

# -------------------------------------------
# 4️⃣ Insert Stores
# -------------------------------------------
print("Inserting stores...")
store_locations = [
    ("New York", "Robert Brown"),
    ("Los Angeles", "Emily Davis"),
    ("Chicago", "Michael Johnson"),
    ("Houston", "Sarah Lee")
]

for loc, mgr in store_locations:
    cursor.execute("""
        INSERT INTO stg.Stores (Location, Manager)
        VALUES (?, ?)
    """, (loc, mgr))

conn.commit()

# -------------------------------------------
# 5️⃣ Insert Sales Transactions
# -------------------------------------------
print("Inserting sales...")

# Get existing IDs for foreign key relationships
cursor.execute("SELECT ProductID FROM stg.Products")
product_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT CustomerID FROM stg.Customers")
customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT StoreID FROM stg.Stores")
store_ids = [row[0] for row in cursor.fetchall()]

for _ in range(200):
    t_date = fake.date_between(start_date='-1y', end_date='today')
    product_id = random.choice(product_ids)
    customer_id = random.choice(customer_ids)
    store_id = random.choice(store_ids)
    quantity = random.randint(1, 10)

    # Get price from Products table
    cursor.execute("SELECT Price FROM stg.Products WHERE ProductID = ?", (product_id,))
    price = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO stg.Sales (TransactionDate, ProductID, CustomerID, StoreID, Quantity, Price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (t_date, product_id, customer_id, store_id, quantity, price))

conn.commit()

# -------------------------------------------
# ✅ Finish Up
# -------------------------------------------
print("✅ Data successfully inserted into staging tables!")

cursor.close()
conn.close()
