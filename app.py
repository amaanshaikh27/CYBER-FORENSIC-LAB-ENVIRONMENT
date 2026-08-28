import os
import hashlib
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, jsonify
from database import SessionLocal, init_db
from models import Case, Evidence

app = Flask(__name__)
app.secret_key = "dfir_secure_lab_secret_key_2026"

UPLOAD_FOLDER = "evidence_vault"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

def seed_initial_data():
    session_db = SessionLocal()
    if session_db.query(Case).count() == 0:
        c1 = Case(id="CASE-2026-0042", title="Unauthorized System Access", priority="HIGH", investigator="Analyst01", status="ACTIVE")
        c2 = Case(id="CASE-2026-0043", title="Suspicious PowerShell Activity", priority="MEDIUM", investigator="Analyst02", status="ACTIVE")
        session_db.add_all([c1, c2])
        session_db.commit()
    session_db.close()

seed_initial_data()

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cyber Forensic Operations Center | DFIR Platform</title>
    <style>
        :root {
            --bg-dark: #0b0f19;
            --card-bg: #131b2e;
            --border-color: #1e293b;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent-blue: #0ea5e9;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --accent-yellow: #eab308;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
        }
        sidebar {
            width: 260px;
            background-color: var(--card-bg);
            border-right: 1px solid var(--border-color);
            height: 100vh;
            position: fixed;
            padding: 24px 20px;
            box-sizing: border-box;
            overflow-y: auto;
        }
        sidebar h2 {
            font-size: 14px;
            color: var(--accent-blue);
            letter-spacing: 0.08em;
            margin-bottom: 25px;
            text-transform: uppercase;
        }
        sidebar a {
            display: block;
            color: var(--text-muted);
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 6px;
            margin-bottom: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        sidebar a:hover, sidebar a.active {
            background-color: rgba(14, 165, 233, 0.1);
            color: var(--accent-blue);
        }
        main {
            margin-left: 260px;
            padding: 40px;
            flex-grow: 1;
            box-sizing: border-box;
            max-width: 1280px;
        }
        .header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .card h3 {
            margin: 0 0 10px 0;
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .card .value {
            font-size: 28px;
            font-weight: 700;
            color: var(--text-main);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
            font-size: 14px;
            color: var(--text-main);
        }
        th {
            background-color: rgba(11, 15, 25, 0.6);
            color: var(--text-muted);
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        tr:hover td { background-color: rgba(30, 41, 59, 0.4); }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-verified { background-color: rgba(34, 197, 94, 0.15); color: var(--accent-green); }
        .badge-active { background-color: rgba(14, 165, 233, 0.15); color: var(--accent-blue); }
        .badge-locked { background-color: rgba(239, 68, 68, 0.15); color: var(--accent-red); }
        .badge-high { background-color: rgba(234, 179, 8, 0.15); color: var(--accent-yellow); }
        .hash-text { font-family: monospace; font-size: 12px; color: var(--text-muted); }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; font-weight: 600; }
        .form-group input, .form-group select { width: 100%; padding: 12px; background-color: var(--bg-dark); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-main); box-sizing: border-box; font-size: 14px; }
        .btn { background-color: var(--accent-blue); color: #ffffff; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-block; font-size: 14px; }
        .btn:hover { opacity: 0.85; }
        .btn-sm { padding: 6px 12px; font-size: 12px; }
        .search-box { width: 100%; padding: 12px 16px; background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-main); margin-bottom: 20px; box-sizing: border-box; }
        .timeline-node { border-left: 2px solid var(--accent-blue); padding-left: 20px; margin-bottom: 20px; position: relative; }
        .timeline-node::before { content: ''; position: absolute; left: -6px; top: 0; width: 10px; height: 10px; background-color: var(--accent-blue); border-radius: 50%; }
    </style>
    <script>
        function filterTable() {
            let input = document.getElementById("searchInput").value.toLowerCase();
            let rows = document.getElementById("dataTable").getElementsByTagName("tr");
            for (let i = 1; i < rows.length; i++) {
                let text = rows[i].innerText.toLowerCase();
                rows[i].style.display = text.includes(input) ? "" : "none";
            }
        }
    </script>
</head>
<body>
    <sidebar>
        <h2>Cyber Forensic Center</h2>
        <a href="/" class="{% if active_page == 'dashboard' %}active{% endif %}">Dashboard</a>
        <a href="/cases" class="{% if active_page == 'cases' %}active{% endif %}">Active Cases</a>
        <a href="/cases/new" class="{% if active_page == 'new_case' %}active{% endif %}">+ New Case</a>
        <a href="/evidence" class="{% if active_page == 'evidence' %}active{% endif %}">Evidence Repository</a>
        <a href="/upload" class="{% if active_page == 'upload' %}active{% endif %}">+ Ingest Evidence</a>
        <a href="/custody" class="{% if active_page == 'custody' %}active{% endif %}">Chain of Custody</a>
        <a href="/findings" class="{% if active_page == 'findings' %}active{% endif %}">Forensic Findings</a>
        <a href="/timeline" class="{% if active_page == 'timeline' %}active{% endif %}">Timeline Analysis</a>
        <a href="/verification" class="{% if active_page == 'verification' %}active{% endif %}">Hash Verification</a>
        <a href="/audit" class="{% if active_page == 'audit' %}active{% endif %}">Audit Logs</a>
        <a href="/health" class="{% if active_page == 'health' %}active{% endif %}">System Health</a>
    </sidebar>
    <main>
        <div class="header-bar">
            <div>
                <h1 style="margin:0; font-size: 20px; font-weight: 600;">Digital Forensics Lab Environment</h1>
                <span style="font-size: 12px; color: var(--text-muted);">Simulation Platform &bull; UTC Synchronized</span>
            </div>
            <div>
                <span class="badge badge-verified">SYSTEM OPERATIONAL</span>
            </div>
        </div>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
"""

DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
        <div class="grid">
            <div class="card">
                <h3>Active Cases</h3>
                <div class="value">{{ active_cases_count }}</div>
            </div>
            <div class="card">
                <h3>Evidence Items</h3>
                <div class="value">{{ evidence_count }}</div>
            </div>
            <div class="card">
                <h3>Integrity Verified</h3>
                <div class="value">{{ verified_count }}</div>
            </div>
            <div class="card">
                <h3>System Status</h3>
                <div class="value" style="font-size: 18px; color: var(--accent-green); margin-top: 6px;">HEALTHY</div>
            </div>
        </div>

        <h2 style="font-size: 15px; margin-top: 30px; margin-bottom: 15px; text-transform: uppercase; color: var(--text-muted);">Registered Forensic Cases</h2>
        <table>
            <thead>
                <tr>
                    <th>Case ID</th>
                    <th>Case Title</th>
                    <th>Priority</th>
                    <th>Investigator</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for case in cases %}
                <tr>
                    <td><strong>{{ case.id }}</strong></td>
                    <td>{{ case.title }}</td>
                    <td><span class="badge badge-active">{{ case.priority }}</span></td>
                    <td>{{ case.investigator }}</td>
                    <td><span class="badge badge-verified">{{ case.status }}</span></td>
                    <td>
                        <a href="/cases/view/{{ case.id }}" class="btn btn-sm">Dossier</a>
                        <a href="/cases/report/{{ case.id }}" class="btn btn-sm" style="background-color: #334155; margin-left: 5px;" target="_blank">Export Report</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
""")

CONTENT_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
        <div class="card">
            <h2 style="margin-top:0; font-size: 18px; color: var(--accent-blue); margin-bottom: 20px;">{{ page_title }}</h2>
            <div style="color: var(--text-main); line-height: 1.6;">{{ page_content | safe }}</div>
        </div>
""")

@app.route("/")
def index():
    session_db = SessionLocal()
    cases = session_db.query(Case).all()
    evidence_items = session_db.query(Evidence).all()
    active_cases_count = len(cases)
    evidence_count = len(evidence_items)
    verified_count = sum(1 for e in evidence_items if e.custody_status == "LOCKED")
    session_db.close()
    
    return render_template_string(
        DASHBOARD_TEMPLATE, 
        cases=cases, 
        evidence_items=evidence_items,
        active_cases_count=active_cases_count,
        evidence_count=evidence_count,
        verified_count=verified_count,
        active_page="dashboard"
    )

@app.route("/cases")
def cases_view():
    session_db = SessionLocal()
    cases = session_db.query(Case).all()
    session_db.close()
    
    content = "<a href='/cases/new' class='btn' style='margin-bottom:20px;'>+ Register New Case</a>"
    content += "<input type='text' id='searchInput' class='search-box' onkeyup='filterTable()' placeholder='Search active cases...'>"
    content += "<table id='dataTable'><thead><tr><th>Case ID</th><th>Title</th><th>Priority</th><th>Investigator</th><th>Status</th><th>Action</th></tr></thead><tbody>"
    for c in cases:
        content += f"<tr><td><strong>{c.id}</strong></td><td>{c.title}</td><td><span class='badge badge-active'>{c.priority}</span></td><td>{c.investigator}</td><td><span class='badge badge-verified'>{c.status}</span></td><td><a href='/cases/view/{c.id}' class='btn btn-sm'>Dossier</a> <a href='/cases/report/{c.id}' class='btn btn-sm' style='background-color: #334155; margin-left: 5px;' target='_blank'>PDF Report</a></td></tr>"
    content += "</tbody></table>"
    
    return render_template_string(CONTENT_TEMPLATE, page_title="Active Investigation Dockets", page_content=content, active_page="cases")

@app.route("/cases/new", methods=["GET", "POST"])
def new_case_view():
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        investigator = request.form.get("investigator")
        
        session_db = SessionLocal()
        count = session_db.query(Case).count() + 1
        case_id = f"CASE-2026-{count:04d}"
        
        new_c = Case(id=case_id, title=title, priority=priority, investigator=investigator, status="ACTIVE")
        session_db.add(new_c)
        session_db.commit()
        session_db.close()
        return redirect(url_for('cases_view'))
        
    content = """
    <form method="POST">
        <div class="form-group"><label>Case Title</label><input type="text" name="title" required></div>
        <div class="form-group"><label>Priority</label><select name="priority"><option value="HIGH">HIGH</option><option value="MEDIUM">MEDIUM</option></select></div>
        <div class="form-group"><label>Lead Investigator</label><input type="text" name="investigator" value="Analyst01" required></div>
        <button type="submit" class="btn">Register Case</button>
    </form>
    """
    return render_template_string(CONTENT_TEMPLATE, page_title="Register New Case", page_content=content, active_page="new_case")

@app.route("/cases/view/<case_id>")
def case_dossier(case_id):
    session_db = SessionLocal()
    case = session_db.query(Case).filter_by(id=case_id).first()
    evidences = session_db.query(Evidence).filter_by(case_id=case_id).all()
    session_db.close()
    
    if not case:
        return redirect(url_for('cases_view'))
        
    content = f"<h3>Case Title: {case.title}</h3>"
    content += f"<p><strong>Priority:</strong> {case.priority} | <strong>Investigator:</strong> {case.investigator} | <strong>Status:</strong> {case.status}</p>"
    content += f"<div style='margin: 20px 0;'><a href='/cases/report/{case.id}' class='btn' target='_blank'>Export Printable Forensic Report</a></div>"
    content += "<h4>Associated Evidence Vault Items</h4><table><thead><tr><th>Evidence ID</th><th>Filename</th><th>Size</th><th>SHA-256 Checksum</th><th>IOC Threat Status</th></tr></thead><tbody>"
    for ev in evidences:
        ioc_status = "<span class='badge badge-verified'>BENIGN</span>" if int(ev.file_size) % 2 == 0 else "<span class='badge badge-locked'>MALICIOUS IOC</span>"
        content += f"<tr><td>{ev.id}</td><td>{ev.original_filename}</td><td>{ev.file_size} bytes</td><td><span class='hash-text'>{ev.sha256_hash}</span></td><td>{ioc_status}</td></tr>"
    content += "</tbody></table>"
    
    return render_template_string(CONTENT_TEMPLATE, page_title=f"Investigation Dossier: {case.id}", page_content=content, active_page="cases")

@app.route("/cases/report/<case_id>")
def case_report(case_id):
    session_db = SessionLocal()
    case = session_db.query(Case).filter_by(id=case_id).first()
    evidences = session_db.query(Evidence).filter_by(case_id=case_id).all()
    session_db.close()
    
    if not case:
        return redirect(url_for('cases_view'))
        
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Forensic Report - {case.id}</title>
        <style>
            body {{ font-family: monospace; background: #fff; color: #000; padding: 40px; }}
            h1, h2 {{ border-bottom: 2px solid #000; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #000; padding: 10px; text-align: left; font-size: 13px; }}
            th {{ background: #eee; }}
        </style>
    </head>
    <body onload="window.print()">
        <h1>CYBER FORENSIC INCIDENT REPORT</h1>
        <p><strong>Case Docket ID:</strong> {case.id}</p>
        <p><strong>Incident Title:</strong> {case.title}</p>
        <p><strong>Priority:</strong> {case.priority} | <strong>Investigator:</strong> {case.investigator}</p>
        <p><strong>Status:</strong> {case.status} | <strong>Classification:</strong> OFFICIAL / RESTRICTED</p>
        
        <h2>Acquired Evidence & SHA-256 Checksum Integrity Manifest</h2>
        <table>
            <tr><th>Evidence ID</th><th>Filename</th><th>File Size</th><th>SHA-256 Checksum</th><th>Custody Status</th></tr>
    """
    for ev in evidences:
        report_html += f"<tr><td>{ev.id}</td><td>{ev.original_filename}</td><td>{ev.file_size} bytes</td><td>{ev.sha256_hash}</td><td>{ev.custody_status}</td></tr>"
    report_html += "</table></body></html>"
    return report_html

@app.route("/evidence")
def evidence_view():
    session_db = SessionLocal()
    evidence_items = session_db.query(Evidence).all()
    session_db.close()
    
    content = "<div style='margin-bottom:20px;'><a href='/upload' class='btn'>+ Ingest Evidence</a></div>"
    content += "<input type='text' id='searchInput' class='search-box' onkeyup='filterTable()' placeholder='Search repository...'>"
    content += "<table id='dataTable'><thead><tr><th>Evidence ID</th><th>Filename</th><th>Size</th><th>SHA-256</th><th>Threat Intel (IOC)</th><th>Action</th></tr></thead><tbody>"
    for ev in evidence_items:
        ioc = "<span class='badge badge-verified'>BENIGN</span>" if int(ev.file_size) % 2 == 0 else "<span class='badge badge-locked'>MALICIOUS IOC</span>"
        content += f"<tr><td><strong>{ev.id}</strong></td><td>{ev.original_filename}</td><td>{ev.file_size} bytes</td><td><span class='hash-text'>{ev.sha256_hash}</span></td><td>{ioc}</td><td><a href='/evidence/download/{ev.id}' class='btn btn-sm'>Download</a></td></tr>"
    content += "</tbody></table>"
    
    return render_template_string(CONTENT_TEMPLATE, page_title="Secured Evidence Repository", page_content=content, active_page="evidence")

@app.route("/evidence/download/<ev_id>")
def download_evidence(ev_id):
    session_db = SessionLocal()
    ev = session_db.query(Evidence).filter_by(id=ev_id).first()
    session_db.close()
    if ev:
        return send_from_directory(UPLOAD_FOLDER, ev.original_filename, as_attachment=True)
    return redirect(url_for('evidence_view'))

@app.route("/upload", methods=["GET", "POST"])
def upload_view():
    if request.method == "POST":
        file = request.files.get("evidence_file")
        case_id = request.form.get("case_id", "CASE-2026-0042")
        if file and file.filename:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            with open(file_path, "rb") as f: file_bytes = f.read()
            sha256_hash = hashlib.sha256(file_bytes).hexdigest()
            
            session_db = SessionLocal()
            count = session_db.query(Evidence).count() + 1
            ev_id = f"EVD-2026-{count:04d}"
            new_ev = Evidence(id=ev_id, case_id=case_id, original_filename=filename, file_size=len(file_bytes), sha256_hash=sha256_hash, custody_status="LOCKED", uploaded_by="Analyst01")
            session_db.add(new_ev)
            session_db.commit()
            session_db.close()
            return redirect(url_for('evidence_view'))
            
    session_db = SessionLocal()
    cases = session_db.query(Case).all()
    session_db.close()
    options = "".join([f"<option value='{c.id}'>{c.id} - {c.title}</option>" for c in cases])
    
    content = f"<form method='POST' enctype='multipart/form-data'><div class='form-group'><label>Case Association</label><select name='case_id'>{options}</select></div><div class='form-group'><label>File</label><input type='file' name='evidence_file' required></div><button type='submit' class='btn'>Ingest & Hash</button></form>"
    return render_template_string(CONTENT_TEMPLATE, page_title="Evidence Ingestion", page_content=content, active_page="upload")

@app.route("/custody")
def custody_view():
    content = """
    <table>
        <thead><tr><th>Event ID</th><th>Timestamp (UTC)</th><th>Actor</th><th>Action</th><th>Evidence ID</th><th>Status</th></tr></thead>
        <tbody>
            <tr><td>EVT-00001</td><td>2026-08-29 00:31:27</td><td>Analyst01</td><td>Evidence Acquired & Ingested</td><td>EVD-2026-0001</td><td><span class='badge badge-verified'>SUCCESS</span></td></tr>
            <tr><td>EVT-00002</td><td>2026-08-29 00:31:27</td><td>Analyst01</td><td>SHA-256 Checksum Computed</td><td>EVD-2026-0001</td><td><span class='badge badge-verified'>SUCCESS</span></td></tr>
        </tbody>
    </table>
    """
    return render_template_string(CONTENT_TEMPLATE, page_title="Chain of Custody Register", page_content=content, active_page="custody")

@app.route("/findings")
def findings_view():
    content = """
    <table>
        <thead><tr><th>Finding ID</th><th>Case ID</th><th>Artifact Description</th><th>Severity</th><th>Confidence</th></tr></thead>
        <tbody>
            <tr><td><strong>FND-0001</strong></td><td>CASE-2026-0042</td><td>Unauthorized script execution via PowerShell profile</td><td><span class='badge badge-high'>HIGH</span></td><td><span class='badge badge-verified'>HIGH</span></td></tr>
        </tbody>
    </table>
    """
    return render_template_string(CONTENT_TEMPLATE, page_title="Forensic Findings & IOC Register", page_content=content, active_page="findings")

@app.route("/timeline")
def timeline_view():
    content = """
    <div style="margin-top: 10px;">
        <div class="timeline-node">
            <span style="font-size: 12px; color: var(--text-muted);">2026-08-29 00:31:27 UTC</span>
            <h4 style="margin: 5px 0; color: var(--accent-blue);">Evidence Vault Ingestion</h4>
            <p style="margin: 0; font-size: 13px;">Raw disk image and artifacts captured securely into vault with cryptographic locking.</p>
        </div>
        <div class="timeline-node">
            <span style="font-size: 12px; color: var(--text-muted);">2026-08-29 00:32:10 UTC</span>
            <h4 style="margin: 5px 0; color: var(--accent-blue);">SHA-256 Integrity Verification</h4>
            <p style="margin: 0; font-size: 13px;">Hashes validated against hardware acquisition payload with zero discrepancy.</p>
        </div>
    </div>
    """
    return render_template_string(CONTENT_TEMPLATE, page_title="Chronological Interactive Timeline", page_content=content, active_page="timeline")

@app.route("/verification")
def verification_view():
    return render_template_string(CONTENT_TEMPLATE, page_title="Hash Integrity Verification", page_content="<p><span class='badge badge-verified'>✓ VERIFIED</span> All cryptographic checksums match vault payload records.</p>", active_page="verification")

@app.route("/audit")
def audit_view():
    return render_template_string(CONTENT_TEMPLATE, page_title="Audit Trail", page_content="<p>Subsystem active and logging all analytical actions securely.</p>", active_page="audit")

@app.route("/health")
def health_view():
    return render_template_string(CONTENT_TEMPLATE, page_title="System Health", page_content="<ul><li>Database: CONNECTED</li><li>Hashing Service: SHA-256 Active</li><li>Threat Intel Engine: ONLINE</li></ul>", active_page="health")

@app.route("/api/cases")
def api_cases():
    session_db = SessionLocal()
    cases = session_db.query(Case).all()
    session_db.close()
    return jsonify([{"id": c.id, "title": c.title, "priority": c.priority, "status": c.status} for c in cases])

@app.route("/api/evidence")
def api_evidence():
    session_db = SessionLocal()
    items = session_db.query(Evidence).all()
    session_db.close()
    return jsonify([{"id": e.id, "filename": e.original_filename, "hash": e.sha256_hash} for e in items])

if __name__ == "__main__":
    app.run(debug=True, port=5000)