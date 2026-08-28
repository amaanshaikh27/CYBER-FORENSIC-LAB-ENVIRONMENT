import os

def scan_for_threats(filename):
    print(f"[*] Running Advanced Threat Intelligence & Signature Scan on '{filename}'...")
    
    # Common malicious indicators or suspicious keywords we look for
    suspicious_signatures = [b"FLAG{", b"malware", b"password", b"hack", b"admin"]
    
    if not os.path.exists(filename):
        print(f"[-] Error: {filename} not found!")
        return

    with open(filename, "rb") as f:
        content = f.read()

    print("\n--- THREAT INTELLIGENCE REPORT ---")
    threat_found = False
    for sig in suspicious_signatures:
        if sig in content:
            print(f"[⚠️] Signature Match Found: {sig.decode()} -> Potential Artifact or Secret Detected!")
            threat_found = True

    if not threat_found:
        print("[✅] Scan Clean: No known malicious signatures detected.")
    else:
        print("\n[🚨] ACTION REQUIRED: Review matched artifacts in your investigation report.")

scan_for_threats("evidence.raw")