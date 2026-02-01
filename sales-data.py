import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Data Preparation
data = {
    'Product': ['Engine Oil 20W-50', 'Industrial Gear Oil', 'Hydraulic Fluid', 'Automotive Grease'],
    'Dhaka': [450, 320, 210, 180],
    'Khulna': [210, 280, 150, 90],
    'Borishal': [120, 90, 80, 60],
    'Sylhet': [180, 140, 110, 85]
}

df = pd.DataFrame(data).set_index('Product')

# Calculations
grand_total_mt = df.values.sum()
top_products = ", ".join(df.index[:4])

# 2. Create a figure with two subplots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
sns.set_theme(style="whitegrid")

# --- SUBPLOT 1: HEATMAP ---
sns.heatmap(df, annot=True, fmt="d", cmap="YlGnBu", ax=ax1, cbar_kws={'label': 'MT'})
ax1.set_title('Sales Density (Heatmap)', fontsize=14)
ax1.set_ylabel('Top 4 Products')

# --- SUBPLOT 2: BAR CHART ---
df.plot(kind='bar', ax=ax2, width=0.8, color=sns.color_palette("viridis", 4))
ax2.set_title('Regional Comparison (Bar Chart)', fontsize=14)
ax2.set_ylabel('Metric Tons (MT)')
ax2.set_xticklabels(df.index, rotation=0)

# Add labels on top of bars
for p in ax2.patches:
    ax2.annotate(str(int(p.get_height())), (p.get_x() + 0.02, p.get_height() + 5), fontsize=9)

# 3. Global Title for the whole dashboard
plt.suptitle(f'GRAND TOTAL: {grand_total_mt} MT\nTop 4 Products: {top_products}', 
             fontsize=10, fontweight='bold', y=1.02)

plt.tight_layout()
plt.title("Total Sales: (2'176)")
plt.show()