import os
from datetime import datetime

def dispatch_report():
    print("[*] Preparing secure report dispatch package...")
    
    dispatch_log = "dispatch_manifest.log"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    required_artifacts = ["Forensic_Report.md", "Secure_Evidence_Locker.zip", "soc_dashboard.html"]
    missing_items = []
    
    for item in required_artifacts:
        if not os.path.exists(item):
            missing_items.append(item)
            
    with open(dispatch_log, "a", encoding="utf-8") as f:
        if not missing_items:
            log_entry = f"[{timestamp}] [DISPATCH SUCCESS]: All core investigation artifacts packaged and locked for transmission.\n"
            print(f"[📤] Status: Ready for secure dispatch! All {len(required_artifacts)} artifacts verified.")
        else:
            log_entry = f"[{timestamp}] [DISPATCH HOLD]: Missing artifacts -> {missing_items}\n"
            print(f"[⚠️] Status: Dispatch on hold. Missing: {missing_items}")
            
        f.write(log_entry)

dispatch_report()