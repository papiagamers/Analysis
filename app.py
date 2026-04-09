import mysql.connector
import matplotlib.pyplot as plt 
# Load environment variables
from dotenv import load_dotenv
import os
import seaborn as sns

load_dotenv()

# Connect to the database
db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
)
cursor = db.cursor()
# Fetch data from the database

cursor.execute("SELECT id, product_name, profit FROM sales_analyst")
data = cursor.fetchall()

# Prepare data for visualization

ids = [row[0] for row in data] 
product_names = [row[1] for row in data]
profits = [row[2] for row in data]

# Create a bar chart to visualize profits by product

plt.figure(figsize=(10, 6))
sns.barplot(x=product_names, y=profits, palette='viridis')
plt.xlabel('Product Name')
plt.ylabel('Profit')
plt.title('Profit by Product')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Area chart to visualize profit trends

cursor.execute("SELECT area, SUM(profit) FROM sales_analyst GROUP BY area")
area_data = cursor.fetchall()

areas = [row[0] for row in area_data]
area_profits = [row[1] for row in area_data]

# Create an area chart to visualize profit trends

plt.figure(figsize=(10, 6))
plt.fill_between(areas, area_profits, color='orange', alpha=0.5)
plt.plot(areas, area_profits, color='orange')
plt.xlabel('Area')
plt.ylabel('Total Profit')
plt.title('Profit Trends by Area')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Making The Customerwise Profit Analysis
cursor.execute("SELECT customer_name, SUM(profit) FROM sales_analyst GROUP BY customer_name")
customer_data = cursor.fetchall()

customer_names = [row[0] for row in customer_data]
customer_profits = [row[1] for row in customer_data]

# Profits by customer

plt.figure(figsize=(10, 6))
sns.barplot(x=customer_names, y=customer_profits, palette='viridis')
plt.xlabel('Customer Name')
plt.ylabel('Total Profit')
plt.title('Profit by Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Target vs Achievement Analysis:
cursor.execute("SELECT target, achievement FROM sales_analyst")
achieve = cursor.fetchall()

target = [row[0] for row in achieve]
achievement = [row[1] for row in achieve]

# visualize target vs achievement

plt.figure(figsize=(10, 6))
plt.bar(range(len(target)), target, color='blue', alpha=0.5, label='Target')
plt.bar(range(len(achievement)), achievement, color='green', alpha=0.5, label='Achievement')
plt.xlabel('Time Period')
plt.ylabel('Amount')
plt.title('Target vs Achievement')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization of The Customer vs Target Achievement
cursor.execute("SELECT customer_name, target, achievement FROM sales_analyst")

customer_achieve = cursor.fetchall()

customer_names = [row[0] for row in customer_achieve]
customer_achievements = [row[2] for row in customer_achieve]

# visualize customer vs achievement

plt.figure(figsize=(10, 6))
plt.bar(range(len(customer_names)), customer_achievements, color='green', alpha=0.5, label='Achievement')
plt.xlabel('Customer Name')
plt.ylabel('Amount')
plt.title('Customer vs Target Achievement')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close the database connection

cursor.close()
db.close()
