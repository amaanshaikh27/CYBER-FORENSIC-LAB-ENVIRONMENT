import hashlib
from datetime import datetime

def calculate_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

file_name = "evidence.raw"
file_hash = calculate_hash(file_name)

# ACPO Audit Log Format
log_entry = f"[{datetime.now()}] EVIDENCE: {file_name} | SHA256: {file_hash}\n"

# Save in permanent log file
with open("audit_log.txt", "a") as log:
    log.write(log_entry)

print("[+] Hash Logged Successfully in audit_log.txt:")
print(log_entry)