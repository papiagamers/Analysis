"""
Supply Chain Management Data Analytics System
Windows/VS Code Compatible Version
Complete system with KPIs, visualizations, and data management
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import matplotlib.pyplot as plt
import os
warnings.filterwarnings('ignore')

# Sample Data Generation
def generate_supply_chain_data(num_records=1000):
    """Generate realistic supply chain data"""
    
    np.random.seed(42)
    
    # Date range
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(num_records)]
    
    # Suppliers
    suppliers = ['Supplier_A', 'Supplier_B', 'Supplier_C', 'Supplier_D', 'Supplier_E']
    
    # Products
    products = ['Product_1', 'Product_2', 'Product_3', 'Product_4', 'Product_5',
                'Product_6', 'Product_7', 'Product_8', 'Product_9', 'Product_10']
    
    # Warehouses
    warehouses = ['Warehouse_North', 'Warehouse_South', 'Warehouse_East', 'Warehouse_West']
    
    # Generate data
    data = {
        'Date': np.random.choice(dates, num_records),
        'Order_ID': [f'ORD{i:05d}' for i in range(1, num_records + 1)],
        'Product': np.random.choice(products, num_records),
        'Supplier': np.random.choice(suppliers, num_records),
        'Warehouse': np.random.choice(warehouses, num_records),
        'Order_Quantity': np.random.randint(10, 500, num_records),
        'Received_Quantity': np.random.randint(10, 500, num_records),
        'Unit_Cost': np.round(np.random.uniform(5, 100, num_records), 2),
        'Lead_Time_Days': np.random.randint(1, 30, num_records),
        'Planned_Lead_Time': np.random.randint(5, 25, num_records),
        'Stock_Level': np.random.randint(0, 1000, num_records),
        'Reorder_Point': np.random.randint(50, 300, num_records),
        'Defect_Quantity': np.random.randint(0, 20, num_records),
        'Transportation_Cost': np.round(np.random.uniform(50, 500, num_records), 2),
        'Order_Status': np.random.choice(['Delivered', 'In Transit', 'Pending', 'Delayed'], 
                                        num_records, p=[0.7, 0.15, 0.1, 0.05])
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived fields
    df['Total_Order_Value'] = df['Order_Quantity'] * df['Unit_Cost']
    df['Fill_Rate'] = (df['Received_Quantity'] / df['Order_Quantity'] * 100).round(2)
    df['On_Time'] = (df['Lead_Time_Days'] <= df['Planned_Lead_Time']).astype(int)
    df['Stockout'] = (df['Stock_Level'] < df['Reorder_Point']).astype(int)
    df['Defect_Rate'] = (df['Defect_Quantity'] / df['Received_Quantity'] * 100).round(2)
    
    return df


class SupplyChainKPIs:
    """Calculate all major Supply Chain KPIs"""
    
    def __init__(self, data):
        self.data = data
        
    def calculate_all_kpis(self):
        """Calculate all KPIs and return as dictionary"""
        
        kpis = {
            # Delivery & Performance KPIs
            'Order_Fill_Rate': self.order_fill_rate(),
            'On_Time_Delivery_Rate': self.on_time_delivery(),
            'Perfect_Order_Rate': self.perfect_order_rate(),
            'Average_Lead_Time': self.average_lead_time(),
            
            # Inventory KPIs
            'Inventory_Turnover': self.inventory_turnover(),
            'Days_of_Inventory': self.days_of_inventory(),
            'Stockout_Rate': self.stockout_rate(),
            
            # Quality KPIs
            'Defect_Rate': self.defect_rate(),
            'Supplier_Quality_Score': self.supplier_quality_score(),
            
            # Cost KPIs
            'Total_Supply_Chain_Cost': self.total_supply_chain_cost(),
            'Average_Order_Value': self.average_order_value(),
            'Cost_Per_Unit': self.cost_per_unit(),
            'Transportation_Cost_Ratio': self.transportation_cost_ratio(),
            
            # Efficiency KPIs
            'Order_Cycle_Time': self.order_cycle_time(),
            'Capacity_Utilization': self.capacity_utilization(),
        }
        
        return kpis
    
    # Delivery & Performance KPIs
    def order_fill_rate(self):
        """Percentage of orders fulfilled completely"""
        return round(self.data['Fill_Rate'].mean(), 2)
    
    def on_time_delivery(self):
        """Percentage of orders delivered on time"""
        return round(self.data['On_Time'].mean() * 100, 2)
    
    def perfect_order_rate(self):
        """Orders delivered complete, on-time, and defect-free"""
        perfect_orders = self.data[
            (self.data['Fill_Rate'] >= 95) & 
            (self.data['On_Time'] == 1) & 
            (self.data['Defect_Rate'] < 1)
        ]
        return round(len(perfect_orders) / len(self.data) * 100, 2)
    
    def average_lead_time(self):
        """Average lead time in days"""
        return round(self.data['Lead_Time_Days'].mean(), 2)
    
    # Inventory KPIs
    def inventory_turnover(self):
        """How many times inventory is sold/used per period"""
        cogs = self.data['Total_Order_Value'].sum()
        avg_inventory = self.data['Stock_Level'].mean() * self.data['Unit_Cost'].mean()
        return round(cogs / avg_inventory if avg_inventory > 0 else 0, 2)
    
    def days_of_inventory(self):
        """Average days of inventory on hand"""
        turnover = self.inventory_turnover()
        return round(365 / turnover if turnover > 0 else 0, 2)
    
    def stockout_rate(self):
        """Percentage of time items are out of stock"""
        return round(self.data['Stockout'].mean() * 100, 2)
    
    # Quality KPIs
    def defect_rate(self):
        """Percentage of defective items"""
        return round(self.data['Defect_Rate'].mean(), 2)
    
    def supplier_quality_score(self):
        """Average supplier quality (100 - defect_rate)"""
        return round(100 - self.defect_rate(), 2)
    
    # Cost KPIs
    def total_supply_chain_cost(self):
        """Total costs across supply chain"""
        total = (self.data['Total_Order_Value'].sum() + 
                self.data['Transportation_Cost'].sum())
        return round(total, 2)
    
    def average_order_value(self):
        """Average value per order"""
        return round(self.data['Total_Order_Value'].mean(), 2)
    
    def cost_per_unit(self):
        """Average cost per unit"""
        return round(self.data['Unit_Cost'].mean(), 2)
    
    def transportation_cost_ratio(self):
        """Transportation cost as % of total order value"""
        trans_cost = self.data['Transportation_Cost'].sum()
        order_value = self.data['Total_Order_Value'].sum()
        return round(trans_cost / order_value * 100 if order_value > 0 else 0, 2)
    
    # Efficiency KPIs
    def order_cycle_time(self):
        """Average time from order to delivery"""
        return self.average_lead_time()
    
    def capacity_utilization(self):
        """Percentage of capacity being used (simulated)"""
        avg_quantity = self.data['Order_Quantity'].mean()
        max_quantity = self.data['Order_Quantity'].max()
        return round(avg_quantity / max_quantity * 100 if max_quantity > 0 else 0, 2)
    
    def get_kpi_summary(self):
        """Return formatted KPI summary"""
        kpis = self.calculate_all_kpis()
        
        summary = "\n" + "="*60
        summary += "\n         SUPPLY CHAIN KPI DASHBOARD"
        summary += "\n" + "="*60 + "\n"
        
        summary += "\n📊 DELIVERY & PERFORMANCE METRICS:\n"
        summary += f"   • Order Fill Rate:          {kpis['Order_Fill_Rate']}%\n"
        summary += f"   • On-Time Delivery:         {kpis['On_Time_Delivery_Rate']}%\n"
        summary += f"   • Perfect Order Rate:       {kpis['Perfect_Order_Rate']}%\n"
        summary += f"   • Average Lead Time:        {kpis['Average_Lead_Time']} days\n"
        
        summary += "\n📦 INVENTORY METRICS:\n"
        summary += f"   • Inventory Turnover:       {kpis['Inventory_Turnover']}x\n"
        summary += f"   • Days of Inventory:        {kpis['Days_of_Inventory']} days\n"
        summary += f"   • Stockout Rate:            {kpis['Stockout_Rate']}%\n"
        
        summary += "\n✅ QUALITY METRICS:\n"
        summary += f"   • Defect Rate:              {kpis['Defect_Rate']}%\n"
        summary += f"   • Supplier Quality Score:   {kpis['Supplier_Quality_Score']}/100\n"
        
        summary += "\n💰 COST METRICS:\n"
        summary += f"   • Total SC Cost:            ${kpis['Total_Supply_Chain_Cost']:,.2f}\n"
        summary += f"   • Average Order Value:      ${kpis['Average_Order_Value']:,.2f}\n"
        summary += f"   • Cost Per Unit:            ${kpis['Cost_Per_Unit']:.2f}\n"
        summary += f"   • Transportation Cost %:    {kpis['Transportation_Cost_Ratio']}%\n"
        
        summary += "\n⚡ EFFICIENCY METRICS:\n"
        summary += f"   • Order Cycle Time:         {kpis['Order_Cycle_Time']} days\n"
        summary += f"   • Capacity Utilization:     {kpis['Capacity_Utilization']}%\n"
        
        summary += "\n" + "="*60 + "\n"
        
        return summary


class SupplyChainAnalytics:
    """Advanced analytics and insights"""
    
    def __init__(self, data):
        self.data = data
    
    def supplier_performance(self):
        """Analyze supplier performance"""
        supplier_stats = self.data.groupby('Supplier').agg({
            'On_Time': 'mean',
            'Fill_Rate': 'mean',
            'Defect_Rate': 'mean',
            'Total_Order_Value': 'sum',
            'Lead_Time_Days': 'mean'
        }).round(2)
        
        supplier_stats.columns = ['On_Time_%', 'Fill_Rate_%', 'Defect_Rate_%', 
                                  'Total_Value', 'Avg_Lead_Time']
        supplier_stats['On_Time_%'] *= 100
        
        return supplier_stats.sort_values('On_Time_%', ascending=False)
    
    def product_performance(self):
        """Analyze product performance"""
        product_stats = self.data.groupby('Product').agg({
            'Order_Quantity': 'sum',
            'Total_Order_Value': 'sum',
            'Defect_Rate': 'mean',
            'Stockout': 'mean'
        }).round(2)
        
        product_stats.columns = ['Total_Quantity', 'Total_Value', 
                                'Avg_Defect_Rate', 'Stockout_Rate']
        product_stats['Stockout_Rate'] *= 100
        
        return product_stats.sort_values('Total_Value', ascending=False)
    
    def warehouse_performance(self):
        """Analyze warehouse performance"""
        warehouse_stats = self.data.groupby('Warehouse').agg({
            'Order_Quantity': 'sum',
            'Stock_Level': 'mean',
            'Stockout': 'mean',
            'Total_Order_Value': 'sum'
        }).round(2)
        
        warehouse_stats.columns = ['Total_Orders', 'Avg_Stock_Level', 
                                   'Stockout_Rate', 'Total_Value']
        warehouse_stats['Stockout_Rate'] *= 100
        
        return warehouse_stats.sort_values('Total_Value', ascending=False)
    
    def monthly_trends(self):
        """Analyze monthly trends"""
        self.data['Month'] = pd.to_datetime(self.data['Date']).dt.to_period('M')
        
        monthly = self.data.groupby('Month').agg({
            'Total_Order_Value': 'sum',
            'Order_Quantity': 'sum',
            'On_Time': 'mean',
            'Defect_Rate': 'mean'
        }).round(2)
        
        monthly.columns = ['Revenue', 'Quantity', 'On_Time_%', 'Defect_Rate']
        monthly['On_Time_%'] *= 100
        
        return monthly
    
    def identify_risks(self):
        """Identify supply chain risks"""
        risks = []
        
        # High defect rate
        high_defects = self.data[self.data['Defect_Rate'] > 5].groupby('Supplier').size()
        if len(high_defects) > 0:
            risks.append(f"⚠️  High defect rates from: {', '.join(high_defects.index.tolist())}")
        
        # Frequent stockouts
        stockout_rate = self.data['Stockout'].mean()
        if stockout_rate > 0.2:
            risks.append(f"⚠️  High stockout rate: {stockout_rate*100:.1f}%")
        
        # Poor on-time delivery
        ontime_rate = self.data['On_Time'].mean()
        if ontime_rate < 0.8:
            risks.append(f"⚠️  Low on-time delivery: {ontime_rate*100:.1f}%")
        
        # Long lead times
        avg_lead = self.data['Lead_Time_Days'].mean()
        if avg_lead > 15:
            risks.append(f"⚠️  Long average lead time: {avg_lead:.1f} days")
        
        if not risks:
            risks.append("✅ No major risks identified")
        
        return "\n".join(risks)


def main():
    """Main execution function"""
    
    # Create output directory if it doesn't exist
    output_dir = 'supply_chain_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("\n🚀 Generating Supply Chain Data...")
    df = generate_supply_chain_data(1000)
    
    print("✅ Data generated successfully!")
    print(f"   Total records: {len(df)}")
    print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Calculate KPIs
    print("\n📊 Calculating KPIs...")
    kpi_calculator = SupplyChainKPIs(df)
    print(kpi_calculator.get_kpi_summary())
    
    # Analytics
    print("\n📈 SUPPLIER PERFORMANCE ANALYSIS:")
    print("="*60)
    analytics = SupplyChainAnalytics(df)
    print(analytics.supplier_performance())
    
    print("\n\n📦 TOP PRODUCTS BY VALUE:")
    print("="*60)
    print(analytics.product_performance().head())
    
    print("\n\n🏭 WAREHOUSE PERFORMANCE:")
    print("="*60)
    print(analytics.warehouse_performance())
    
    print("\n\n📅 MONTHLY TRENDS:")
    print("="*60)
    monthly = analytics.monthly_trends()
    monthly.index = monthly.index.astype(str)  # Convert Period to string
    print(monthly)
    
    print("\n\n⚠️  RISK ANALYSIS:")
    print("="*60)
    print(analytics.identify_risks())
    
    # Save data
    print("\n\n💾 Saving data...")
    df.to_csv(f'{output_dir}/supply_chain_data.csv', index=False)
    print(f"✅ Data saved to: {output_dir}/supply_chain_data.csv")
    
    # Save KPIs
    kpis = kpi_calculator.calculate_all_kpis()
    kpi_df = pd.DataFrame([kpis])
    kpi_df.to_csv(f'{output_dir}/supply_chain_kpis.csv', index=False)
    print(f"✅ KPIs saved to: {output_dir}/supply_chain_kpis.csv")
    
    # Save analytics reports
    supplier_perf = analytics.supplier_performance()
    supplier_perf.to_csv(f'{output_dir}/supplier_performance.csv')
    print(f"✅ Supplier report saved to: {output_dir}/supplier_performance.csv")
    
    product_perf = analytics.product_performance()
    product_perf.to_csv(f'{output_dir}/product_performance.csv')
    print(f"✅ Product report saved to: {output_dir}/product_performance.csv")
    
    print("\n✨ Supply Chain Analytics System Complete!")
    print(f"   All files saved in '{output_dir}' folder")
    
    return df, kpi_calculator, analytics


if __name__ == "__main__":
    df, kpis, analytics = main()
    print("\n🎯 Ready! Use 'df' for data, 'kpis' for KPIs, 'analytics' for insights")
plt.show()
