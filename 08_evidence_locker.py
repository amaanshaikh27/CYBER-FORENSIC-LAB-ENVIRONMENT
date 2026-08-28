import zipfile
import os

def create_evidence_locker():
    zip_name = "Secure_Evidence_Locker.zip"
    files_to_pack = ["evidence.raw", "audit_log.txt", "Forensic_Report.md"]
    
    print("[*] Packing all investigation files into secure archive...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_pack:
            if os.path.exists(file):
                zipf.write(file)
                print(f"[+] Added to locker: {file}")
            else:
                print(f"[-] Warning: {file} not found!")

    print(f"\n[✅] Success! Secure Evidence Locker created: {zip_name}")

create_evidence_locker()