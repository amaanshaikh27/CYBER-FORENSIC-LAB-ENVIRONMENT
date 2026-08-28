import os
from datetime import datetime

def get_file_timeline(filename):
    # File ke system timestamps nikalna (Creation aur Modification)
    stats = os.stat(filename)
    created_time = datetime.fromtimestamp(stats.st_ctime)
    modified_time = datetime.fromtimestamp(stats.st_mtime)
    
    print("--- EVIDENCE TIMELINE ANALYSIS ---")
    print(f"[⏱️] File Created At: {created_time}")
    print(f"[⏱️] File Modified At: {modified_time}")

    # Timeline ko audit log mein bhi save karna
    timeline_log = f"\n[TIMELINE] File: {filename} | Created: {created_time} | Modified: {modified_time}\n"
    with open("audit_log.txt", "a") as log:
        log.write(timeline_log)

get_file_timeline("evidence.raw")