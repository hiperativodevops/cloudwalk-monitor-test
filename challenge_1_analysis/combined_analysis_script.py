import pandas as pd
import matplotlib.pyplot as plt

# --- 1. ANALYSIS OF CHECKOUT_1.CSV (PRIMARY SALES ANOMALY) ---
print("--- 1. Analyzing checkout_1.csv: Hourly Sales Volume ---")
df_c1 = pd.read_csv("checkout_1.csv")

# Data preparation and calculation of deviation vs. weekly average
df_c1['sort_key'] = df_c1['time'].str.replace('h', '').astype(int)
df_c1 = df_c1.sort_values('sort_key').drop('sort_key', axis=1)
df_c1['deviation_vs_avg_week'] = df_c1['today'] - df_c1['avg_last_week']

# Critical Anomaly #1: Morning Drops (08h and 09h)
largest_drops_c1 = df_c1.sort_values(by='deviation_vs_avg_week', ascending=True).head(3)
print("Anomaly #1 (Morning Drop):")
print(largest_drops_c1[['time', 'today', 'avg_last_week', 'deviation_vs_avg_week']])


# --- 2. ANALYSIS OF CHECKOUT_2.CSV ---
print("\n--- 2. Analyzing checkout_2.csv: Secondary Anomaly Check ---")
df_c2 = pd.read_csv("checkout_2.csv")

# Data preparation and calculation of deviation vs. weekly average
df_c2['deviation_vs_avg_week'] = df_c2['today'] - df_c2['avg_last_week']

# Critical Anomaly #2: Afternoon Drops (15h, 16h, 17h)
largest_drops_c2 = df_c2.sort_values(by='deviation_vs_avg_week', ascending=True).head(5)
print("Anomaly #2 (Afternoon Drop - Recurring Failure):")
print(largest_drops_c2[['time', 'today', 'avg_last_week', 'deviation_vs_avg_week']])
print("\nConclusion: System shows multiple, critical points of failure throughout the day.")


# ---3. GRAPHIC GENERATION ---
plt.figure(figsize=(12, 6))

plt.plot(df_c1['time'], df_c1['today'], marker='o', linestyle='-', color='red', label='Today (Sales)')
plt.plot(df_c1['time'], df_c1['yesterday'], marker='s', linestyle='--', color='blue', label='Yesterday (Sales)')
plt.plot(df_c1['time'], df_c1['avg_last_week'], marker='^', linestyle=':', color='green', label='Avg Last Week (Baseline)')

# Highlight Anomaly Region #1 (08h and 09h)
plt.axvspan('07h', '10h', color='yellow', alpha=0.3, label='Morning Anomaly Region')
# Highlight Anomaly Region #2 (15h to 17h, using the second CSV's finding)
plt.axvspan('14h', '18h', color='orange', alpha=0.2, label='Afternoon Anomaly Region (Ref: Csv 2)')

# Configure labels
plt.title('POS Sales by Hour: Today vs. Historical Baselines (Multiple Anomalies Detected)', fontsize=14)
plt.xlabel('Time of Day (Hour)', fontsize=12)
plt.ylabel('Number of POS Sales', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, which='major', linestyle='--', linewidth=0.5)
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('sales_anomaly_chart.png')
print("\nChart 'sales_anomaly_chart.png' generated successfully, highlighting both failure periods.")