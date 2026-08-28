# Dummy evidence file generate karne ke liye script
with open("evidence.raw", "wb") as f:
    # Header / Dummy Normal Data
    f.write(b"CONFIDENTIAL COMPANY DATA - SYSTEM LOGS\n")
    f.write(b"User: Admin | Action: Login | Status: Success\n")
    f.write(b"=" * 50 + b"\n")
    
    # Hidden / Simulated Deleted Secret Data
    f.write(b"FLAG{PASSWORD_EXFILTRATED_SECRET_KEY_9988}\n")
    f.write(b"DELETED_FILE_MARKER: Secret plan text here.\n")

print("[+] Evidence file 'evidence.raw' successfully created!")