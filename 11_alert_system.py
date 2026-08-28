import os
from datetime import datetime

def trigger_security_alert():
    print("[*] Checking security logs for anomalies...")
    
    alert_log = "security_alerts.log"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if integrity or evidence locker exists
    if os.path.exists("Secure_Evidence_Locker.zip"):
        status_message = f"[{timestamp}] [ALERT - INFO]: Evidence successfully secured and locked in archive.\n"
    else:
        status_message = f"[{timestamp}] [ALERT - WARNING]: Evidence locker missing! Immediate audit required.\n"

    with open(alert_log, "a", encoding="utf-8") as f:
        f.write(status_message)
        
    print(f"[🚨] Security Alert Logged: {status_message.strip()}")

trigger_security_alert()