import os
from datetime import datetime
import hashlib
from database import SessionLocal, init_db
from models import Case, Evidence

def init_forensic_environment():
    init_db()
    session = SessionLocal()
    
    # 1. Create a Sample DFIR Case if not exists
    case_id = "CASE-2026-0042"
    existing_case = session.query(Case).filter_by(id=case_id).first()
    
    if not existing_case:
        print(f"[*] Creating Forensic Case: {case_id}")
        new_case = Case(
            id=case_id,
            title="Unauthorized System Access",
            description="Investigation into unauthorized lateral movement and privilege escalation.",
            priority="HIGH",
            status="ACTIVE",
            investigator="Analyst01"
        )
        session.add(new_case)
        session.commit()
    
    # 2. Ingest Sample Evidence and Calculate SHA-256
    evidence_id = "EVD-2026-0001"
    existing_evidence = session.query(Evidence).filter_by(id=evidence_id).first()
    
    target_file = "evidence.raw"
    if not os.path.exists(target_file):
        with open(target_file, "wb") as f:
            f.write(b"SIMULATED_FORENSIC_DISK_IMAGE_DATA_PAYLOAD")
            
    if not existing_evidence:
        print(f"[*] Ingesting Evidence Item: {evidence_id}")
        
        # Calculate SHA-256 Hash
        sha256_hash = hashlib.sha256()
        with open(target_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
        file_size = os.path.getsize(target_file)
        
        new_evidence = Evidence(
            id=evidence_id,
            case_id=case_id,
            original_filename=target_file,
            file_size=file_size,
            sha256_hash=file_hash,
            custody_status="LOCKED",
            acquisition_time=datetime.utcnow()
        )
        session.add(new_evidence)
        session.commit()
        print(f"[✅] Evidence Ingested & Locked! SHA-256: {file_hash}")
    else:
        print(f"[ℹ️] Evidence {evidence_id} already registered in database.")
        
    session.close()

if __name__ == "__main__":
    init_forensic_environment()