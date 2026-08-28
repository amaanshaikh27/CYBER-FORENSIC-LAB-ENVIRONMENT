import re

def carve_evidence(filename):
    print(f"[*] Scanning '{filename}' for forensic artifacts...")
    
    with open(filename, 'rb') as f:
        content = f.read()

    # Pattern Matching for hidden flags & deleted strings
    flags = re.findall(rb"FLAG\{.*?\}", content)
    deleted_text = re.findall(rb"DELETED_FILE_MARKER:.*?\n", content)

    print("\n--- RECOVERED ARTIFACTS ---")
    for flag in flags:
        print(f"[!] Secret Key Found: {flag.decode('utf-8')}")
    for text in deleted_text:
        print(f"[!] Recovered Text: {text.decode('utf-8').strip()}")

carve_evidence("evidence.raw")