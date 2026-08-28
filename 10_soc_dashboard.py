import os
from datetime import datetime

def generate_soc_dashboard():
    print("[*] Generating Enterprise SOC HTML Dashboard...")
    
    audit_data = "No logs recorded yet."
    if os.path.exists("audit_log.txt"):
        with open("audit_log.txt", "r", encoding="utf-8") as f:
            audit_data = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Forensic SOC Dashboard</title>
    <style>
        :root {{
            --bg-color: #090d16;
            --card-bg: #111827;
            --accent-green: #10b981;
            --accent-blue: #0ea5e9;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: #1f2937;
        }}
        body {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 30px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            font-size: 24px;
            color: var(--accent-blue);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        }}
        .card h3 {{
            margin-top: 0;
            font-size: 14px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .status-badge {{
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        .log-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 25px;
            border-radius: 12px;
        }}
        .log-card h2 {{
            font-size: 18px;
            margin-top: 0;
            color: var(--text-main);
        }}
        pre {{
            background: #030712;
            padding: 15px;
            border-radius: 8px;
            color: #34d399;
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            overflow-x: auto;
            border: 1px solid #111827;
            max-height: 350px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ Cyber Forensic Operations Center</h1>
            <span class="status-badge">● SYSTEM SECURE</span>
        </header>

        <div class="grid">
            <div class="card">
                <h3>Generated Timestamp</h3>
                <p style="font-size: 16px; font-weight: 500; margin: 5px 0;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <div class="card">
                <h3>Active Workspace</h3>
                <p style="font-size: 16px; font-weight: 500; margin: 5px 0;">Forensic_Lab (Local)</p>
            </div>
        </div>

        <div class="log-card">
            <h2>Live Audit Trail & Chain of Custody</h2>
            <pre>{audit_data}</pre>
        </div>
    </div>
</body>
</html>
"""

    with open("soc_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("[✅] Modern SOC Dashboard generated successfully: soc_dashboard.html")

generate_soc_dashboard()