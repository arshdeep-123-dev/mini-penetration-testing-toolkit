# 🛡️ Mini Penetration Testing Toolkit

**Detect. Analyze. Secure.**

A Flask-based web application that performs basic penetration testing on web applications by analyzing URLs, detecting common vulnerabilities, checking SSL certificates, scanning ports, and generating a PDF security report.

> **Disclaimer:** This toolkit is intended **only for educational purposes and authorized security testing**. Do **not** scan websites or systems without explicit permission from the owner.

---

# 📌 Project Overview

The Mini Penetration Testing Toolkit automates several fundamental web security checks through a simple web interface. It combines multiple security modules into a single application and provides an overall security risk score along with a downloadable PDF report.

This project was developed as part of a Cyber Security academic project to demonstrate practical web vulnerability assessment techniques.

---

# ✨ Features

- ✅ URL Scanner
- ✅ HTTP/HTTPS Detection
- ✅ Security Header Analysis
- ✅ Open Port Scanner
- ✅ SQL Injection Detection
- ✅ Cross-Site Scripting (XSS) Detection
- ✅ SSL Certificate Checker
- ✅ Security Risk Score Calculation
- ✅ PDF Security Report Generation
- ✅ Simple Flask Web Interface

---

# 🛠️ Tech Stack

### Backend

- Python
- Flask

### Libraries

- Requests
- BeautifulSoup4
- ReportLab
- Socket
- SSL
- urllib.parse

### Frontend

- HTML
- CSS

---

# 📂 Project Structure

```
mini-penetration-testing-toolkit/

├── app.py
├── risk_score.py
├── requirements.txt
├── Procfile
├── README.md
│
├── reports/
│
├── scanners/
│   ├── url_scanner.py
│   ├── port_scanner.py
│   ├── sql_scanner.py
│   ├── xss_scanner.py
│   ├── ssl_checker.py
│   └── dvwa_helper.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
└── utils/
    └── report_generator.py
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/arshdeep-123-dev/mini-penetration-testing-toolkit.git
```

Go inside the project folder.

```bash
cd mini-penetration-testing-toolkit
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python app.py
```

Open your browser.

```
http://127.0.0.1:5000
```

---

# 🚀 How to Use

1. Enter a target URL.
2. Click **Scan**.
3. The toolkit performs:
   - URL Analysis
   - Port Scan
   - Security Header Check
   - SQL Injection Detection
   - XSS Detection
   - SSL Analysis
   - Risk Score Calculation
4. View the results on the webpage.
5. Download the PDF security report.

---

# 🔍 Modules

## 1. URL Scanner

Performs:

- HTTP Status Code
- Redirect Detection
- Server Information
- HTTPS Detection
- Security Header Analysis

Example Output:

```
Status Code : 200

HTTPS : Enabled

Missing Headers:

X-Frame-Options

Content-Security-Policy
```

---

## 2. Port Scanner

Scans commonly used ports.

Example:

```
80   HTTP

443  HTTPS

3306 MySQL
```

---

## 3. SQL Injection Detection

The toolkit automatically:

- Detects HTML forms
- Identifies GET/POST methods
- Sends common SQL payloads
- Compares responses
- Detects possible SQL Injection indicators

Example Result

```
Potential SQL Injection

Reason:

SQL-related response detected after payload
```

---

## 4. Cross-Site Scripting (XSS) Detection

The toolkit:

- Detects forms
- Injects XSS payloads
- Checks reflected responses

Example

```
No XSS indicators detected.
```

---

## 5. SSL Checker

Checks:

- Certificate validity
- Issuer
- Expiry date
- Remaining validity

Example

```
Status : Valid

Issuer : DigiCert

Days Remaining : 138
```

---

## 6. Security Risk Score

The toolkit calculates an overall security score based on detected vulnerabilities.

Current scoring model:

| Finding | Score |
|---------|------:|
| SQL Injection | +40 |
| XSS | +30 |
| Missing Security Header | +5 each |
| Invalid / Missing SSL | +10 |

Risk Levels:

| Score | Risk |
|------:|------|
| 0 | Secure 🟢 |
| 1–39 | Low Risk 🟡 |
| 40–69 | Medium Risk 🟠 |
| 70–100 | High Risk 🔴 |

---

# 📄 PDF Report

The generated PDF includes:

- Target URL
- Security Risk Score
- Risk Level
- SQL Injection Results
- XSS Results
- SSL Analysis
- Detected Issues

---

# 🧪 Testing

## DVWA (Damn Vulnerable Web Application)

The toolkit was tested on DVWA running locally to verify vulnerability detection.

### SQL Injection Module

Target:

```
http://localhost/dvwa/vulnerabilities/sqli/
```

Result:

- Successfully detected SQL Injection indicators.
- Risk Score increased accordingly.

### XSS Module

Target:

```
http://localhost/dvwa/vulnerabilities/xss_r/
```

Result:

- Successfully tested reflected XSS detection.

---

## Public Website Testing

Example:

```
https://www.zomato.com
```

Observed:

- Valid SSL Certificate
- No SQL Injection Indicators
- No XSS Indicators
- Security Headers analyzed
- Low Risk Score generated

---

# 📸 Screenshots

Add screenshots here.

Suggested screenshots:

- Home Page
- URL Scan Result
- SQL Injection Detection
- XSS Detection
- SSL Checker
- Risk Score
- PDF Report
- DVWA SQL Injection Test
- DVWA XSS Test

---

# 🔒 Disclaimer

This project is intended **only for educational purposes** and authorized penetration testing.

The developer is **not responsible** for misuse of this software.

Always obtain permission before scanning any website or server.

---

# 🚀 Future Improvements

- Nmap Integration
- Directory Enumeration
- CSRF Detection
- Clickjacking Detection
- Authentication Testing
- OWASP Top 10 Coverage
- Export Reports in HTML Format
- Dashboard with Scan History
- Multi-threaded Scanning
- API Version
- Docker Support

---

# 👨‍💻 Author

**Arshdeep Kaur**

B.Tech Computer Science Engineering (Cyber Security)

---

# ⭐ Acknowledgements

- Flask
- Requests
- BeautifulSoup
- ReportLab
- DVWA (Damn Vulnerable Web Application)
- OWASP