CloudWalk Monitoring Analyst Challenge
This repository contains the technical assessment deliverables for the CloudWalk Monitoring Analyst position. 
The challenge is executed in two main parts: Data Analysis for Anomaly Detection (3.1) and Real-Time Alert System Implementation (3.2).

1. Challenge 3.1: Get Your Hands Dirty - Anomaly Analysis
This section analyzes POS sales data (checkout_1.csv and checkout_2.csv) to identify anomalies and infer the potential business impact ("business fire").

1.1. Anomaly Findings and Conclusion
Analysis revealed a pattern of recurring, critical system failures throughout the day, suggesting deep instability rather than a single isolated incident.
<img width="559" height="46" alt="image" src="https://github.com/user-attachments/assets/5bb6e486-fc7d-47b5-82f6-b2b190c2c26a" />

Business Fire Conclusion:
The system is experiencing sporadic but complete outages, resulting in 90% to 100% loss of sales volume during key operating hours (08h, 09h, 15h-17h). 
This demands an immediate, high-priority alert and root cause analysis, likely pointing to an intermittent configuration error or a cascading service failure. 
The monitoring system implemented in Challenge 3.2 must be sensitive enough to detect these immediate drops.

1.2. Visualization (Graphic)
The line chart below, generated using data from checkout_1.csv and augmented with findings from checkout_2.csv, visually highlights both critical failure periods 
compared to historical baselines.

(Note: The sales_anomaly_chart.png file is located in the challenge_1_analysis/ folder.)

1.3. SQL Query for Anomaly Detection
To quickly organize and filter the data in a production environment, the following SQL query sorts sales volume by the magnitude of the drop against the weekly average, 
surfacing critical failures instantly:

SELECT time, today, avg_last_week, (today - avg_last_week) AS deviation, Calculate the percentage difference to determine the severity (the anomaly score)
    ROUND((today - avg_last_week) * 100.0 / avg_last_week, 2) AS percentage_deviation
FROM sales_data_table
WHERE  ABS(today - avg_last_week) > 5 
ORDER BY deviation ASC;

