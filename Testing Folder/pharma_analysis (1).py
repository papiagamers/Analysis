import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Generate pharmaceutical company data for Bangladesh
np.random.seed(42)

# Define medicines (popular in Bangladesh)
medicines = [
    'Napa (Paracetamol)',
    'Ace (Paracetamol)',
    'Seclo (Omeprazole)',
    'Alatrol (Cetirizine)',
    'Sergel (Sertraline)',
    'Fexo (Fexofenadine)',
    'Monas (Montelukast)',
    'Maxpro (Esomeprazole)',
    'Flexi (Meloxicam)',
    'Tory (Torsemide)'
]

# Define salesmen
salesmen = [
    'Karim Ahmed',
    'Rahim Uddin',
    'Fatima Begum',
    'Nasir Hossain',
    'Sultana Akter',
    'Jamal Khan',
    'Nadia Islam',
    'Rafiq Miah'
]

# Define regions in Bangladesh
regions = ['Dhaka', 'Chittagong', 'Sylhet', 'Rajshahi', 'Khulna', 'Barisal', 'Rangpur', 'Mymensingh']

# Generate data for January and February 2026
data = []
months = ['January', 'February']
month_nums = [1, 2]

for month, month_num in zip(months, month_nums):
    for day in range(1, 29):  # 28 days for simplicity
        num_transactions = np.random.randint(15, 30)
        
        for _ in range(num_transactions):
            medicine = np.random.choice(medicines)
            salesman = np.random.choice(salesmen)
            region = np.random.choice(regions)
            
            # Different price ranges for different medicines
            if 'Napa' in medicine or 'Ace' in medicine:
                price = np.random.uniform(1.5, 3.0)
            elif 'Seclo' in medicine or 'Maxpro' in medicine:
                price = np.random.uniform(5.0, 8.0)
            else:
                price = np.random.uniform(3.0, 12.0)
            
            quantity = np.random.randint(10, 200)
            total_sale = price * quantity
            
            data.append({
                'Date': f'2026-{month_num:02d}-{day:02d}',
                'Month': month,
                'Medicine': medicine,
                'Salesman': salesman,
                'Region': region,
                'Unit_Price': round(price, 2),
                'Quantity': quantity,
                'Total_Sale': round(total_sale, 2)
            })

# Create DataFrame
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

print("="*80)
print("BANGLADESH PHARMACEUTICAL COMPANY DATA ANALYSIS")
print("="*80)
print(f"\nTotal Records: {len(df)}")
print(f"Date Range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"\nDataset Preview:")
print(df.head(10))

# Save to CSV
df.to_csv('pharma_data.csv', index=False)
print(f"\n✓ Data saved to: pharma_data.csv")

# ========================================
# ANALYSIS 1: TOP 3 MEDICINES
# ========================================
print("\n" + "="*80)
print("TOP 3 MEDICINES ANALYSIS")
print("="*80)

# Overall Top 3
top_medicines = df.groupby('Medicine').agg({
    'Total_Sale': 'sum',
    'Quantity': 'sum'
}).sort_values('Total_Sale', ascending=False).head(3)

print("\nOverall Top 3 Medicines (January & February):")
print("-" * 60)
for idx, (medicine, row) in enumerate(top_medicines.iterrows(), 1):
    print(f"{idx}. {medicine}")
    print(f"   Total Sales: ৳{row['Total_Sale']:,.2f}")
    print(f"   Units Sold: {row['Quantity']:,}")
    print()

# Top 3 by Month
print("\nTop 3 Medicines by Month:")
print("-" * 60)
for month in months:
    month_data = df[df['Month'] == month]
    top_month = month_data.groupby('Medicine')['Total_Sale'].sum().sort_values(ascending=False).head(3)
    print(f"\n{month} 2026:")
    for idx, (medicine, sale) in enumerate(top_month.items(), 1):
        print(f"  {idx}. {medicine}: ৳{sale:,.2f}")

# ========================================
# ANALYSIS 2: SALESMAN ANALYSIS
# ========================================
print("\n" + "="*80)
print("SALESMAN PERFORMANCE ANALYSIS")
print("="*80)

# Overall Salesman Performance
salesman_performance = df.groupby('Salesman').agg({
    'Total_Sale': 'sum',
    'Quantity': 'sum',
    'Date': 'count'
}).rename(columns={'Date': 'Transactions'}).sort_values('Total_Sale', ascending=False)

print("\nOverall Salesman Performance (January & February):")
print("-" * 80)
print(f"{'Rank':<6}{'Salesman':<20}{'Total Sales':<20}{'Units Sold':<15}{'Transactions':<15}")
print("-" * 80)
for idx, (salesman, row) in enumerate(salesman_performance.iterrows(), 1):
    print(f"{idx:<6}{salesman:<20}৳{row['Total_Sale']:>13,.2f}{row['Quantity']:>14,}{row['Transactions']:>14,}")

# Monthly Salesman Performance
print("\n\nMonthly Salesman Performance:")
print("-" * 80)
for month in months:
    print(f"\n{month} 2026 - Top 5 Salesmen:")
    month_data = df[df['Month'] == month]
    monthly_sales = month_data.groupby('Salesman')['Total_Sale'].sum().sort_values(ascending=False).head(5)
    
    for idx, (salesman, sale) in enumerate(monthly_sales.items(), 1):
        print(f"  {idx}. {salesman}: ৳{sale:,.2f}")

# ========================================
# VISUALIZATION
# ========================================
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS...")
print("="*80)

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 1. Top 3 Medicines Bar Chart
ax1 = plt.subplot(3, 2, 1)
top_3_overall = df.groupby('Medicine')['Total_Sale'].sum().sort_values(ascending=False).head(3)
bars = ax1.bar(range(len(top_3_overall)), top_3_overall.values, color=['#2ecc71', '#3498db', '#e74c3c'])
ax1.set_xlabel('Medicine', fontweight='bold')
ax1.set_ylabel('Total Sales (৳)', fontweight='bold')
ax1.set_title('Top 3 Medicines by Sales', fontweight='bold', fontsize=14)
ax1.set_xticks(range(len(top_3_overall)))
ax1.set_xticklabels(top_3_overall.index, rotation=15, ha='right')
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'৳{height:,.0f}', ha='center', va='bottom', fontsize=9)

# 2. Top Salesmen Bar Chart
ax2 = plt.subplot(3, 2, 2)
top_5_salesmen = salesman_performance.head(5)
bars = ax2.barh(range(len(top_5_salesmen)), top_5_salesmen['Total_Sale'].values, 
                color=sns.color_palette("viridis", 5))
ax2.set_yticks(range(len(top_5_salesmen)))
ax2.set_yticklabels(top_5_salesmen.index)
ax2.set_xlabel('Total Sales (৳)', fontweight='bold')
ax2.set_title('Top 5 Salesmen Performance', fontweight='bold', fontsize=14)
ax2.invert_yaxis()
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width + width*0.02, bar.get_y() + bar.get_height()/2.,
            f'৳{width:,.0f}', ha='left', va='center', fontsize=9)

# 3. Monthly Sales Comparison
ax3 = plt.subplot(3, 2, 3)
monthly_sales = df.groupby('Month')['Total_Sale'].sum()
colors = ['#3498db', '#e74c3c']
bars = ax3.bar(monthly_sales.index, monthly_sales.values, color=colors)
ax3.set_xlabel('Month', fontweight='bold')
ax3.set_ylabel('Total Sales (৳)', fontweight='bold')
ax3.set_title('Monthly Sales Comparison', fontweight='bold', fontsize=14)
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'৳{height:,.0f}', ha='center', va='bottom', fontsize=10)

# 4. Sales by Region
ax4 = plt.subplot(3, 2, 4)
region_sales = df.groupby('Region')['Total_Sale'].sum().sort_values(ascending=False)
ax4.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%',
        startangle=90, colors=sns.color_palette("Set3", len(region_sales)))
ax4.set_title('Sales Distribution by Region', fontweight='bold', fontsize=14)

# 5. Daily Sales Trend
ax5 = plt.subplot(3, 2, 5)
daily_sales = df.groupby('Date')['Total_Sale'].sum()
ax5.plot(daily_sales.index, daily_sales.values, marker='o', linewidth=2, markersize=4)
ax5.set_xlabel('Date', fontweight='bold')
ax5.set_ylabel('Total Sales (৳)', fontweight='bold')
ax5.set_title('Daily Sales Trend', fontweight='bold', fontsize=14)
ax5.grid(True, alpha=0.3)
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 6. Medicine Category Distribution
ax6 = plt.subplot(3, 2, 6)
medicine_count = df.groupby('Medicine')['Quantity'].sum().sort_values(ascending=False).head(8)
ax6.barh(range(len(medicine_count)), medicine_count.values, color=sns.color_palette("coolwarm", len(medicine_count)))
ax6.set_yticks(range(len(medicine_count)))
ax6.set_yticklabels(medicine_count.index)
ax6.set_xlabel('Units Sold', fontweight='bold')
ax6.set_title('Top 8 Medicines by Units Sold', fontweight='bold', fontsize=14)
ax6.invert_yaxis()

plt.tight_layout()
plt.savefig('pharma_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("\n✓ Dashboard saved to: pharma_analysis_dashboard.png")

# ========================================
# SUMMARY REPORT
# ========================================
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)

total_revenue = df['Total_Sale'].sum()
total_units = df['Quantity'].sum()
avg_transaction = df['Total_Sale'].mean()

print(f"\nTotal Revenue: ৳{total_revenue:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Average Transaction Value: ৳{avg_transaction:,.2f}")
print(f"Total Transactions: {len(df):,}")
print(f"\nBest Performing Region: {region_sales.idxmax()} (৳{region_sales.max():,.2f})")
print(f"Best Performing Salesman: {salesman_performance.index[0]} (৳{salesman_performance['Total_Sale'].iloc[0]:,.2f})")
print(f"Best Selling Medicine: {top_medicines.index[0]} (৳{top_medicines['Total_Sale'].iloc[0]:,.2f})")

# Month-over-Month Growth
jan_sales = df[df['Month'] == 'January']['Total_Sale'].sum()
feb_sales = df[df['Month'] == 'February']['Total_Sale'].sum()
growth = ((feb_sales - jan_sales) / jan_sales) * 100

print(f"\nMonth-over-Month Growth: {growth:+.2f}%")
print(f"  January Sales: ${jan_sales:,.2f}")
print(f"  February Sales: ${feb_sales:,.2f}")

print("\n" + "="*80)
print("Analysis Complete! Files generated:")
print("  1. pharma_data.csv - Complete dataset")
print("  2. pharma_analysis_dashboard.png - Visual dashboard")
print("="*80)
plt.show()