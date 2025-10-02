import pandas as pd
import matplotlib.pyplot as plt

# Define the threshold used in the anomaly model
FAILURE_ALERT_THRESHOLD = 0.03  # 3.0%

# Load the data (We'll use Today's sales count as a PROXY for Total Transactions)
df = pd.read_csv("checkout_2.csv")

# --- SIMULATE FAILURE RATE for VISUALIZATION ---
# In a real scenario, this data would come from a database.
# Here, we simulate a constant historical average failure rate of 2% for demonstration.
df['simulated_failure_rate'] = 0.02 * (1 + (df['today'] - df['today'].mean()) / df['today'].std() * 0.1)
df.loc[8:10, 'simulated_failure_rate'] = [0.035, 0.045, 0.025] # Manually inject an anomaly for visibility

# --- GENERATE PLOT ---
plt.figure(figsize=(12, 6))

# Plot the metric (Simulated Failure Rate)
plt.plot(df['time'], df['simulated_failure_rate'] * 100, marker='o', linestyle='-', color='red', label='Simulated Failure Rate (%)')

# Plot the Alert Threshold (The Rule)
plt.axhline(FAILURE_ALERT_THRESHOLD * 100, color='blue', linestyle='--', linewidth=2, label=f'Alert Threshold ({FAILURE_ALERT_THRESHOLD*100:.1f}%)')

# Highlight the anomaly where the line crosses the threshold
plt.axvspan('08h', '10h', color='yellow', alpha=0.3)

# Configuration
plt.title('Real-Time Alerting Concept: Failure Rate vs. Alert Threshold', fontsize=14)
plt.xlabel('Time of Day (Hour)', fontsize=12)
plt.ylabel('Rate (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, which='major', linestyle='--', linewidth=0.5)
plt.legend(loc='upper right')

plt.tight_layout()
plt.savefig('realtime_monitoring_chart.png')
print("Visualization chart 'realtime_monitoring_chart.png' generated successfully.")