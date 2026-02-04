"""
Supply Chain Dashboard - Windows/VS Code Compatible
Creates visual charts for KPI monitoring
Run this in VS Code on Windows!
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from supply_chain_analytics_windows import generate_supply_chain_data, SupplyChainKPIs

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

# Create output directory
output_dir = 'supply_chain_output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate data
print("📊 Loading supply chain data...")
df = generate_supply_chain_data(1000)
kpis = SupplyChainKPIs(df)

# Create comprehensive dashboard
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Supply Chain Management Dashboard', fontsize=20, fontweight='bold', y=0.995)

# 1. KPI Summary (Top section)
ax1 = plt.subplot(4, 4, 1)
kpi_data = kpis.calculate_all_kpis()
kpi_metrics = [
    f"Fill Rate\n{kpi_data['Order_Fill_Rate']}%",
    f"On-Time\n{kpi_data['On_Time_Delivery_Rate']}%",
    f"Perfect Order\n{kpi_data['Perfect_Order_Rate']}%"
]
colors_kpi = ['#2ecc71' if kpi_data['Order_Fill_Rate'] > 90 else '#e74c3c',
              '#2ecc71' if kpi_data['On_Time_Delivery_Rate'] > 90 else '#e74c3c',
              '#2ecc71' if kpi_data['Perfect_Order_Rate'] > 90 else '#e74c3c']
ax1.bar(range(3), [kpi_data['Order_Fill_Rate'], kpi_data['On_Time_Delivery_Rate'], 
                   kpi_data['Perfect_Order_Rate']], color=colors_kpi, alpha=0.7)
ax1.set_xticks(range(3))
ax1.set_xticklabels(['Fill Rate', 'On-Time', 'Perfect Order'], fontsize=9)
ax1.set_ylabel('Percentage (%)', fontsize=10)
ax1.set_title('Delivery Performance', fontweight='bold', fontsize=11)
ax1.axhline(y=90, color='green', linestyle='--', alpha=0.5, label='Target: 90%')
ax1.legend(fontsize=8)

# 2. Inventory Metrics
ax2 = plt.subplot(4, 4, 2)
inv_metrics = ['Turnover\n' + str(kpi_data['Inventory_Turnover']) + 'x',
               'Days Inv\n' + str(kpi_data['Days_of_Inventory']) + 'd',
               'Stockout\n' + str(kpi_data['Stockout_Rate']) + '%']
inv_values = [kpi_data['Inventory_Turnover'], kpi_data['Days_of_Inventory'], 
              kpi_data['Stockout_Rate']]
ax2.bar(range(3), inv_values, color=['#3498db', '#9b59b6', '#e67e22'], alpha=0.7)
ax2.set_xticks(range(3))
ax2.set_xticklabels(['Turnover', 'Days Inv', 'Stockout %'], fontsize=9)
ax2.set_ylabel('Value', fontsize=10)
ax2.set_title('Inventory Health', fontweight='bold', fontsize=11)

# 3. Quality Metrics
ax3 = plt.subplot(4, 4, 3)
quality_labels = ['Defect Rate', 'Quality Score']
quality_values = [kpi_data['Defect_Rate'], kpi_data['Supplier_Quality_Score']]
colors_quality = ['#e74c3c', '#2ecc71']
ax3.bar(range(2), quality_values, color=colors_quality, alpha=0.7)
ax3.set_xticks(range(2))
ax3.set_xticklabels(quality_labels, fontsize=9)
ax3.set_ylabel('Score', fontsize=10)
ax3.set_title('Quality Metrics', fontweight='bold', fontsize=11)

# 4. Cost Overview (Pie Chart)
ax4 = plt.subplot(4, 4, 4)
cost_labels = ['Order Value', 'Transportation']
cost_values = [kpi_data['Total_Supply_Chain_Cost'] * 0.98, 
               kpi_data['Total_Supply_Chain_Cost'] * 0.02]
colors_cost = ['#3498db', '#e67e22']
ax4.pie(cost_values, labels=cost_labels, autopct='%1.1f%%', colors=colors_cost, startangle=90)
ax4.set_title('Cost Distribution', fontweight='bold', fontsize=11)

# 5. Supplier Performance
ax5 = plt.subplot(4, 4, 5)
supplier_perf = df.groupby('Supplier')['On_Time'].mean().sort_values(ascending=True) * 100
supplier_perf.plot(kind='barh', ax=ax5, color='steelblue', alpha=0.7)
ax5.set_xlabel('On-Time Delivery (%)', fontsize=10)
ax5.set_ylabel('Supplier', fontsize=10)
ax5.set_title('Supplier On-Time Performance', fontweight='bold', fontsize=11)
ax5.axvline(x=90, color='green', linestyle='--', alpha=0.5)

# 6. Product Performance
ax6 = plt.subplot(4, 4, 6)
product_value = df.groupby('Product')['Total_Order_Value'].sum().sort_values(ascending=False).head(5)
product_value.plot(kind='bar', ax=ax6, color='coral', alpha=0.7)
ax6.set_xlabel('Product', fontsize=10)
ax6.set_ylabel('Total Value ($)', fontsize=10)
ax6.set_title('Top 5 Products by Value', fontweight='bold', fontsize=11)
ax6.tick_params(axis='x', rotation=45)

# 7. Warehouse Stock Levels
ax7 = plt.subplot(4, 4, 7)
warehouse_stock = df.groupby('Warehouse')['Stock_Level'].mean()
warehouse_stock.plot(kind='bar', ax=ax7, color='lightgreen', alpha=0.7)
ax7.set_xlabel('Warehouse', fontsize=10)
ax7.set_ylabel('Avg Stock Level', fontsize=10)
ax7.set_title('Warehouse Stock Levels', fontweight='bold', fontsize=11)
ax7.tick_params(axis='x', rotation=45)

# 8. Lead Time Distribution
ax8 = plt.subplot(4, 4, 8)
ax8.hist(df['Lead_Time_Days'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
ax8.set_xlabel('Lead Time (Days)', fontsize=10)
ax8.set_ylabel('Frequency', fontsize=10)
ax8.set_title('Lead Time Distribution', fontweight='bold', fontsize=11)
ax8.axvline(x=df['Lead_Time_Days'].mean(), color='red', linestyle='--', 
            label=f'Avg: {df["Lead_Time_Days"].mean():.1f}d')
ax8.legend(fontsize=8)

# 9. Monthly Order Trend
ax9 = plt.subplot(4, 4, 9)
df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
monthly_orders = df.groupby('Month')['Order_ID'].count()
monthly_orders.index = monthly_orders.index.astype(str)
monthly_orders.plot(ax=ax9, color='teal', marker='o', linewidth=2)
ax9.set_xlabel('Month', fontsize=10)
ax9.set_ylabel('Number of Orders', fontsize=10)
ax9.set_title('Monthly Order Volume Trend', fontweight='bold', fontsize=11)
ax9.tick_params(axis='x', rotation=45)
ax9.grid(True, alpha=0.3)

# 10. Monthly Revenue Trend
ax10 = plt.subplot(4, 4, 10)
monthly_revenue = df.groupby('Month')['Total_Order_Value'].sum()
monthly_revenue.index = monthly_revenue.index.astype(str)
monthly_revenue.plot(ax=ax10, color='green', marker='s', linewidth=2)
ax10.set_xlabel('Month', fontsize=10)
ax10.set_ylabel('Revenue ($)', fontsize=10)
ax10.set_title('Monthly Revenue Trend', fontweight='bold', fontsize=11)
ax10.tick_params(axis='x', rotation=45)
ax10.grid(True, alpha=0.3)

# 11. Defect Rate by Supplier
ax11 = plt.subplot(4, 4, 11)
defect_by_supplier = df.groupby('Supplier')['Defect_Rate'].mean().sort_values(ascending=False)
defect_by_supplier.plot(kind='bar', ax=ax11, color='salmon', alpha=0.7)
ax11.set_xlabel('Supplier', fontsize=10)
ax11.set_ylabel('Avg Defect Rate (%)', fontsize=10)
ax11.set_title('Defect Rate by Supplier', fontweight='bold', fontsize=11)
ax11.tick_params(axis='x', rotation=45)
ax11.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='Threshold: 5%')
ax11.legend(fontsize=8)

# 12. Order Status Distribution
ax12 = plt.subplot(4, 4, 12)
order_status = df['Order_Status'].value_counts()
colors_status = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
ax12.pie(order_status, labels=order_status.index, autopct='%1.1f%%', 
         colors=colors_status, startangle=90)
ax12.set_title('Order Status Distribution', fontweight='bold', fontsize=11)

# 13. Fill Rate vs Order Quantity Scatter
ax13 = plt.subplot(4, 4, 13)
sample_df = df.sample(min(200, len(df)))
scatter = ax13.scatter(sample_df['Order_Quantity'], sample_df['Fill_Rate'], 
                       c=sample_df['On_Time'], cmap='RdYlGn', alpha=0.6, s=50)
ax13.set_xlabel('Order Quantity', fontsize=10)
ax13.set_ylabel('Fill Rate (%)', fontsize=10)
ax13.set_title('Order Quantity vs Fill Rate', fontweight='bold', fontsize=11)
plt.colorbar(scatter, ax=ax13, label='On-Time (1=Yes)')

# 14. Transportation Cost by Warehouse
ax14 = plt.subplot(4, 4, 14)
trans_cost = df.groupby('Warehouse')['Transportation_Cost'].sum()
trans_cost.plot(kind='bar', ax=ax14, color='orange', alpha=0.7)
ax14.set_xlabel('Warehouse', fontsize=10)
ax14.set_ylabel('Total Trans. Cost ($)', fontsize=10)
ax14.set_title('Transportation Cost by Warehouse', fontweight='bold', fontsize=11)
ax14.tick_params(axis='x', rotation=45)

# 15. Stockout Analysis
ax15 = plt.subplot(4, 4, 15)
stockout_by_product = df.groupby('Product')['Stockout'].mean().sort_values(ascending=False).head(5) * 100
stockout_by_product.plot(kind='barh', ax=ax15, color='crimson', alpha=0.7)
ax15.set_xlabel('Stockout Rate (%)', fontsize=10)
ax15.set_ylabel('Product', fontsize=10)
ax15.set_title('Top 5 Products - Stockout Risk', fontweight='bold', fontsize=11)

# 16. Capacity Utilization Gauge
ax16 = plt.subplot(4, 4, 16)
capacity = kpi_data['Capacity_Utilization']
categories = ['Low\n(<50%)', 'Medium\n(50-80%)', 'High\n(>80%)']
values = [50, 30, 20] if capacity < 50 else ([0, 50, 50] if capacity < 80 else [0, 0, 100])
colors_cap = ['#e74c3c', '#f39c12', '#2ecc71']
bars = ax16.bar(range(3), [50, 30, 20], color=colors_cap, alpha=0.3)
current_idx = 0 if capacity < 50 else (1 if capacity < 80 else 2)
bars[current_idx].set_alpha(0.9)
ax16.set_xticks(range(3))
ax16.set_xticklabels(categories, fontsize=9)
ax16.set_ylabel('Utilization Range', fontsize=10)
ax16.set_title(f'Capacity Utilization: {capacity}%', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(f'{output_dir}/supply_chain_dashboard.png', dpi=300, bbox_inches='tight')
print(f"✅ Dashboard saved as: {output_dir}/supply_chain_dashboard.png")

# Create a simplified single-page KPI dashboard
fig2, axes = plt.subplots(2, 3, figsize=(16, 10))
fig2.suptitle('Supply Chain KPI Summary Dashboard', fontsize=18, fontweight='bold')

# Key metrics display
kpi_summary = [
    ('Fill Rate', kpi_data['Order_Fill_Rate'], '%'),
    ('On-Time Delivery', kpi_data['On_Time_Delivery_Rate'], '%'),
    ('Defect Rate', kpi_data['Defect_Rate'], '%'),
    ('Avg Lead Time', kpi_data['Average_Lead_Time'], 'days'),
    ('Inventory Turnover', kpi_data['Inventory_Turnover'], 'x'),
    ('Stockout Rate', kpi_data['Stockout_Rate'], '%')
]

for idx, (ax, (name, value, unit)) in enumerate(zip(axes.flat, kpi_summary)):
    # Determine color based on metric
    if 'Rate' in name or 'Delivery' in name or 'Fill' in name:
        color = '#2ecc71' if value > 85 else '#e74c3c'
    elif 'Defect' in name or 'Stockout' in name:
        color = '#2ecc71' if value < 10 else '#e74c3c'
    else:
        color = '#3498db'
    
    ax.text(0.5, 0.6, f"{value}", fontsize=48, ha='center', va='center', 
            color=color, fontweight='bold')
    ax.text(0.5, 0.35, unit, fontsize=16, ha='center', va='center', color='gray')
    ax.text(0.5, 0.15, name, fontsize=14, ha='center', va='center', 
            fontweight='bold', wrap=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Add border
    for spine in ax.spines.values():
        spine.set_edgecolor('lightgray')
        spine.set_linewidth(2)
        spine.set_visible(True)

plt.tight_layout()
plt.savefig(f'{output_dir}/kpi_summary_dashboard.png', dpi=300, bbox_inches='tight')
print(f"✅ KPI Summary saved as: {output_dir}/kpi_summary_dashboard.png")

print("\n🎨 Dashboards created successfully!")
print(f"   • {output_dir}/supply_chain_dashboard.png - Comprehensive view")
print(f"   • {output_dir}/kpi_summary_dashboard.png - Quick KPI overview")
print(f"\n📂 Open the '{output_dir}' folder to view your files!")