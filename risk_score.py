def calculate_risk_score(results):
    
    score = 0
    issues = []

    # SQL Injection
    sql_results = results.get("sql_results", [])

    for item in sql_results:
        if item.get("Status") == "Potential SQL Injection":
            score += 40
            issues.append("SQL Injection vulnerability detected")
            break


    # XSS
    xss_results = results.get("xss_results", [])

    for item in xss_results:
        if item.get("Status") in ["Potential XSS", "XSS Detected"]:
            score += 30
            issues.append("Cross-Site Scripting (XSS) detected")
            break


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


    # SSL Check
    ssl = results.get("ssl_result", {})

    ssl_status = ssl.get("Status")


    if ssl_status == "Not Enabled ❌":
        score += 10
        issues.append("SSL certificate issue")


    # Ignore timeout/error cases
    # Error does not equal vulnerability


    # Maximum score
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