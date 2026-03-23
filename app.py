"""                MADED BY TASNIMUL CODER! PLEASE REVIEW US"""

import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


query = "SELECT viscosity_index, brand_name FROM lubricants"
df = pd.read_sql(query, db)

plt.figure(figsize=(8, 5))
plt.bar(df['viscosity_index'], df['brand_name'], color='orange')
plt.title('Lubricant Prices by Brand')
plt.xlabel('Price (BDT)')
plt.ylabel('Brand Name')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

query1 = "SELECT stock_quantity, product_name FROM lubricants"
df = pd.read_sql(query1, db)

plt.figure(figsize=(8, 6))
plt.bar(df["stock_quantity"], df["product_name"], color='red')
plt.title("Lubricants Stock By Product")
plt.xlabel('Stock')
plt.ylabel('Product')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

query2 = "SELECT brand_name, viscosity_grade FROM lubricants"
df = pd.read_sql(query2, db)

plt.figure(figsize=(8, 6))
plt.bar(df["viscosity_grade"], df["brand_name"], color='blue')
plt.title("Lubricants Brand By Viscosity")
plt.xlabel('Brand')
plt.ylabel('Product')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
db.close()
