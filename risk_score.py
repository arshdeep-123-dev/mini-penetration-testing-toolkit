def calculate_risk_score(results):
    
    score = 0
    issues = []

    # SQL Injection
    if results.get("sql_results"):
        score += 40
        issues.append("SQL Injection vulnerability detected")

    # XSS
    if results.get("xss_results"):
        score += 30
        issues.append("Cross-Site Scripting (XSS) detected")


    # Security Headers
    headers = results.get("headers", {})

    missing_headers = {
        "X-Frame-Options":
            "Clickjacking protection missing",
        "Content-Security-Policy":
            "Content Security Policy missing",
        "Strict-Transport-Security":
            "HTTPS enforcement missing",
        "X-Content-Type-Options":
            "MIME sniffing protection missing"
    }

    for header, message in missing_headers.items():
        if header not in headers:
            score += 5
            issues.append(message)
            
            
    # SSL issue
    ssl = results.get("ssl_result", {})
    if ssl.get("Status") != "Valid ✅":
        score += 10
        issues.append("SSL certificate issue")

     # Limit score
    if score > 100:
        score = 100

    # Risk Level
    if score >= 70:
        level = "High Risk 🔴"
    elif score >= 40:
        level = "Medium Risk 🟠"
    elif score > 0:
        level = "Low Risk 🟡"
    else:
        level = "Secure 🟢"


    return {
        "score": score,
        "level": level,
        "issues": issues
    }