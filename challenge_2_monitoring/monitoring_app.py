import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- STATISTICAL RULE-BASED MODEL (Based on Historical Data) ---
# Alert thresholds are defined using the 3-Sigma rule (Mean + 3 * Std Dev)
THRESHOLDS = {
    'failed_rate': 0.03,    # Alert if failed transactions exceed 3.0%
    'denied_rate': 0.08,    # Alert if denied transactions exceed 8.0%
    'reversed_rate': 0.008  # Alert if reversed transactions exceed 0.8%
}

def check_for_anomaly(data: dict) -> dict:
    """
    Receives current transaction data and applies the rule-based model.
    """
    alerts = []
    
    # 1. Input Validation and Rate Calculation
    try:
        total_txns = data.get('total_transactions', 0)
        
        # Check if total_txns is zero to avoid division by zero error
        if total_txns == 0:
            return {"status": "OK", "recommendation": "LOW_VOLUME", "alerts": []}
            
        current_failed_rate = data.get('failed_count', 0) / total_txns
        current_denied_rate = data.get('denied_count', 0) / total_txns
        current_reversed_rate = data.get('reversed_count', 0) / total_txns
        
    except TypeError:
        return {"status": "ERROR", "recommendation": "INVALID_DATA", "alerts": ["Input data is malformed."]}

    # 2. Apply Rules (Alert Logic)
    if current_failed_rate > THRESHOLDS['failed_rate']:
        alerts.append(f"HIGH_FAILURE: Rate ({current_failed_rate:.2%}) exceeded threshold ({THRESHOLDS['failed_rate']:.2%}).")

    if current_denied_rate > THRESHOLDS['denied_rate']:
        alerts.append(f"HIGH_DENIAL: Rate ({current_denied_rate:.2%}) exceeded threshold ({THRESHOLDS['denied_rate']:.2%}).")
        
    if current_reversed_rate > THRESHOLDS['reversed_rate']:
        alerts.append(f"HIGH_REVERSED: Rate ({current_reversed_rate:.2%}) exceeded threshold ({THRESHOLDS['reversed_rate']:.2%}).")
        
    # 3. Automatic Reporting System
    if alerts:
        # In a real system, this would call Slack/PagerDuty/Email API.
        # Here, we simulate the automatic report.
        print(f"!!! ALERT INCIDENT TRIGGERED: {alerts}")
        return {"status": "ALERT", "recommendation": "P0_INCIDENT_TRIGGERED", "alerts": alerts}
    else:
        return {"status": "OK", "recommendation": "System is operating within normal parameters.", "alerts": []}


# --- THE MONITORING ENDPOINT ---
@app.route('/api/v1/monitor_txn', methods=['POST'])
def monitor_transaction_data():
    """
    Receives real-time transaction aggregates (per minute) and returns an alert recommendation.
    Expected Input JSON: {"total_transactions": 100, "failed_count": 5, "denied_count": 10, "reversed_count": 0}
    """
    data = request.get_json()
    result = check_for_anomaly(data)
    
    return jsonify(result)

if __name__ == '__main__':
    # Running the Flask server on Windows
    print("Monitoring System API is running on http://127.0.0.1:5000/")
    app.run(debug=True)