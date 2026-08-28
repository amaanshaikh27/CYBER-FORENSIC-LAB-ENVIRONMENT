# Cyber Forensic Operations Center & DFIR Platform

An enterprise-grade, web-based digital forensics and incident response (DFIR) laboratory environment built with Flask and SQLAlchemy. Designed to simulate and manage full-lifecycle security incidents, the platform features cryptographic evidence integrity verification, automated threat intelligence IOC scanning, and comprehensive case dossier management.

## Key Architecture & Technical Capabilities

* **Evidence Vault & Cryptography**: Securely ingests digital artifacts, automatically computing SHA-256 cryptographic checksums to enforce tamper-evident chain of custody tracking.
* **Threat Intelligence Engine**: Automatically scans ingested evidence against simulated Indicators of Compromise (IOCs) to instantly categorize files as benign or malicious.
* **Automated Forensic Reporting**: Generates real-time, print-ready forensic incident reports and case dockets containing immutable audit logs and checksum manifests.
* **Modular Codebase**: Engineered following clean architecture principles, separating routing (`app.py`), relational database schemas (`models.py`), and persistence layers (`database.py`).

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/amaanshaikh27/CYBER-FORENSIC-LAB-ENVIRONMENT.git](https://github.com/amaanshaikh27/CYBER-FORENSIC-LAB-ENVIRONMENT.git)
   cd CYBER-FORENSIC-LAB-ENVIRONMENT
   Git clone: ⁠git clone [https://github.com/amaanshaikh27/CYBER-FORENSIC-LAB-ENVIRONMENT.git](https://github.com/amaanshaikh27/CYBER-FORENSIC-LAB-ENVIRONMENT.git)⁠
 Directory shift: ⁠cd CYBER-FORENSIC-LAB-ENVIRONMENT⁠
 Dependency installation: ⁠pip install -r requirements.txt⁠
 App launch: ⁠python app.py
