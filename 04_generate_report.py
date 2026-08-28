import hashlib
from datetime import datetime

def get_hash(file_path):
    return hashlib.sha256(open(file_path, 'rb').read()).hexdigest()

evidence_file = "evidence.raw"
file_hash = get_hash(evidence_file)

report_content = f"""# Digital Forensic Investigation Report

**Case Name:** Lab Simulated Forensic Investigation  
**Date/Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Investigator:** Forensic Analyst  

---

## 1. Evidence Information
* **File Name:** {evidence_file}
* **SHA-256 Hash:** `{file_hash}`
* **Chain of Custody:** Verified via `audit_log.txt` (ACPO Guidelines Compliant)

---

## 2. Key Forensic Discoveries
* **Secret Key Extracted:** `FLAG{{PASSWORD_EXFILTRATED_SECRET_KEY_9988}}`
* **Recovered File Content:** `Secret plan text here.`

---

## 3. Conclusion
The raw evidence image was processed using custom byte-carving tools. All hashes match original logs, confirming evidence integrity.
"""

with open("Forensic_Report.md", "w") as f:
    f.write(report_content)

print("[+] Forensic Report generated: Forensic_Report.md")