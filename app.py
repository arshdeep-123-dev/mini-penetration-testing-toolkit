import requests
import os

from scanners.dvwa_helper import login_to_dvwa

from flask import Flask, render_template, request
from urllib.parse import urlparse

from scanners.url_scanner import scan_url
from scanners.port_scanner import scan_ports
from scanners.sql_scanner import scan_sql
from scanners.xss_scanner import scan_xss
from scanners.ssl_checker import check_ssl
from risk_score import calculate_risk_score

from flask import Flask, render_template, request, send_file
from utils.report_generator import generate_report

app = Flask(__name__)
latest_report = {}

@app.route("/", methods=["GET", "POST"])

def home():

    url_result = None
    port_result = None
    sql_result = None
    xss_result = None
    ssl_result = None
    risk = None

    if request.method == "POST":
        
        url = request.form["url"]
        
        session = requests.Session()
        
        if "localhost/dvwa" in url:
            login_to_dvwa(session)
       
        print(session.cookies.get_dict())
        
        url_result = scan_url(url)

        # Extract hostname from URL
        hostname = urlparse(url).hostname

        if hostname:
            port_result = scan_ports(hostname)
        
        sql_result = scan_sql(url, session)
        print("SQL RESULTS:", sql_result)
        
        xss_result = scan_xss(url, session)
        print("Returned XSS:", xss_result)
        
        ssl_result = check_ssl(url)
        print("SSL RESULT:", ssl_result)
        
        results = {
            "sql_results": sql_result,
            "xss_results": xss_result,
            "ssl_result": ssl_result,
            "headers": url_result
        }  
        risk = calculate_risk_score(results)
        print("RISK SCORE:", risk)
        
        global latest_report
        latest_report = {
            "url": url,
            "risk": risk,
            "sql_result": sql_result,
            "xss_result": xss_result,
            "ssl_result": ssl_result
        }
        print("REPORT DATA:", latest_report)

    return render_template(
        "index.html", 
        url_result=url_result,
        port_result=port_result,
        sql_result=sql_result,
        xss_result=xss_result,
        ssl_result=ssl_result,
        risk=risk
    )
    
@app.route("/download-report")
def download_report():
    if not latest_report:
        return "No scan data available. Please scan a URL first."

    os.makedirs("reports", exist_ok=True)

    filename = "reports/security_report.pdf"
    
    generate_report(
        filename,
        latest_report
    )
    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
    