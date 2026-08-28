import hashlib

def verify_evidence_integrity(filename, original_known_hash):
    print(f"[*] Verifying integrity for '{filename}'...")
    
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    current_hash = sha256.hexdigest()

    print(f"[🔍] Current Hash: {current_hash}")
    
    if current_hash == original_known_hash:
        print("[✅] INTEGRITY VERIFIED: Evidence is untampered and clean!")
    else:
        print("[❌] WARNING: EVIDENCE HAS BEEN MODIFIED OR CORRUPTED!")

# Step 2 wala original hash yahan paste kiya hai
known_hash = "68baee03b15a3cce71b5ed93f5b3e9f408a57e529e0a97aee35d15665091f49d"
verify_evidence_integrity("evidence.raw", known_hash)