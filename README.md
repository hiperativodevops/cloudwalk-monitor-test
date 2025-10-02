# CloudWalk Monitoring Analyst Challenge

This repository contains the technical assessment deliverables for the CloudWalk Monitoring Analyst position. The challenge is executed in two main parts: Data Analysis for Anomaly Detection (3.1) and Real-Time Alert System Implementation (3.2).

## 1. Challenge 3.1: Get Your Hands Dirty - Anomaly Analysis

This analysis examines hourly POS sales data from both provided CSVs to identify anomalies and infer the potential business impact ("business fire"). The baseline is defined by the avg_last_week metric.

### 1.1. Anomaly Findings and Conclusion

Cross-referencing checkout_1.csv and checkout_2.csv revealed a pattern of *recurring, critical system failures* throughout the day, indicating deep instability rather than a single, isolated incident.

| Anomaly Period | Data Source | Sales Metric (Today) | Baseline (Avg Last Week) | Deviation | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| *Morning Outage* | checkout_1.csv | *0 and 2* transactions (08h & 09h) | 8.71 and 20.00 | *$-18.00$* | *CRITICAL (P0)* |
| *Afternoon Outage* | checkout_2.csv | *0* transactions (15h, 16h, 17h) | 22.43, 21.57, 17.71 | *$-22.43$* | *CRITICAL (P0)* |

*Business Fire Conclusion:*
The system experienced *sporadic but complete outages, resulting in **$90\%$ to $100\%$ loss of sales volume* during crucial operating hours. This severity demands an immediate, *high-priority alert* and root cause analysis. The monitoring system implemented in Challenge 3.2 must be sensitive enough to detect these instantaneous drops.

### 1.2. Visualization (Graphic)

The chart below visualizes the severe drops in "Today's Sales" compared to the historical averages, with highlighted regions indicating the confirmed failure times.

sales_anomaly_chart.png is located in the challenge_1_analysis/ folder.

### 1.3. SQL Query for Anomaly Detection

This SQL query is designed to quickly surface the most critical operational issues by calculating the percentage deviation and sorting the results to show the largest sales drops first.

```sql
SELECT
    time,
    today,
    avg_last_week,
    -- Calculate the absolute difference in sales
    (today - avg_last_week) AS deviation,
    -- Calculate the percentage difference to determine the severity
    ROUND((today - avg_last_week) * 100.0 / avg_last_week, 2) AS percentage_deviation
FROM
    sales_data_table
WHERE
    ABS(today - avg_last_week) > 5 -- Filters for substantial absolute drops/spikes
ORDER BY
    deviation ASC; -- Order to show the largest DROPS (negative deviation) first
```

## 2. Challenge 3.2: Solve the Problem - Monitoring System Implementation

A real-time monitoring and alerting system was implemented using *Python/Flask* with a *Statistical Rule-Based Model*. The system meets all requirements by analyzing incoming transaction status data (failed, denied, reversed) against predefined thresholds.

### 2.1. System Architecture and Anomaly Model

| Component | Technology / Concept | Function |
| :--- | :--- | :--- |
| *API Endpoint* | Python (Flask) | POST /api/v1/monitor_txn. Receives aggregated transaction counts per minute. |
| *Anomaly Model* | *Statistical Rule-Based (3-Sigma)* | Compares current failure rates to a historical mean ($\mu$) plus three standard deviations ($\mu + 3\sigma$). This ensures alerts fire only on significant deviations from normal operating conditions. |
| *Automatic Reporting* | Python print() / Conceptual Logging | The check_for_anomaly function automatically logs a P0 incident when an alert is triggered, simulating a notification to teams (e.g., Slack, PagerDuty). |

*Defined Alert Thresholds (3-Sigma):*
* *Failed Rate:* $3.0\%$
* *Denied Rate:* $8.0\%$
* *Reversed Rate:* $0.8\%$

### 2.2. Query and Visualization

*Real-Time Monitoring Query (PromQL Concept):*
In a production environment, time-series databases are used. This PromQL query calculates the failure rate in a rolling window to detect real-time anomalies:

```promql
# PromQL Query to track the 5-minute average rate of failed transactions
(sum by (status) (rate(transaction_count_total{status="failed"}[5m])))
/
(sum by (status) (rate(transaction_count_total[5m])))
> 0.03
```

Visualization Concept:
The chart below illustrates how a simulated failure rate operates relative to the Alert Threshold (blue dashed line). Any data point exceeding the threshold triggers a CRITICAL alert.

realtime_monitoring_chart.png is located in the challenge_2_monitoring/ folder.
