import os

def audit_workspace():
    print("[*] Auditing Forensic Lab Workspace...")
    total_size = 0
    file_count = 0
    
    print("\n--- FILE MANIFEST ---")
    for filename in os.listdir("."):
        if os.path.isfile(filename):
            file_size = os.path.getsize(filename)
            total_size += file_size
            file_count += 1
            print(f"[📄] File: {filename} | Size: {file_size} bytes")

    print(f"\n[📊] Total Files in Lab: {file_count}")
    print(f"[📦] Total Workspace Size: {total_size} bytes")

audit_workspace()