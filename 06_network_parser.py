import re

def parse_network_artifacts(filename):
    print(f"[*] Scanning '{filename}' for IP addresses and Emails...")
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')

    # Regex patterns for IP and Email
    ip_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', content)

    print("\n--- NETWORK & COMMUNICATION ARTIFACTS ---")
    print(f"[🌐] Found IP Addresses: {set(ip_addresses)}")
    print(f"[📧] Found Email Addresses: {set(emails)}")

parse_network_artifacts("evidence.raw")