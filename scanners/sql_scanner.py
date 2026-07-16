import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

session = requests.Session()

# Common database error messages
SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "mysql_fetch",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql syntax",
    "sqlite error",
    "postgresql",
    "odbc",
    "ora-"
]

# Simple benign test values
TEST_VALUES = [
    "1",
    "'",
    "1' OR '1'='1",
    "1 OR 1=1"
]


def clean_response(html):
    
    html = re.sub(
        r'value="[a-z0-9]{32}"',
        'value="TOKEN"',
        html
    )

    return html

def dvwa_login(base_url):
    
    login_url = urljoin(base_url, "login.php")
    
    # Step 1: Get login page
    response = session.get(login_url, timeout=5)
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )
    token = soup.find(
        "input",
        {"name": "user_token"}
    )
    if token:
        user_token = token["value"]
    else:
        user_token = ""

    # Step 2: Submit login
    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token
    }

    response = session.post(
        login_url,
        data=data,
        timeout=5
    )

    # Debug
    print("Login URL:", response.url)

    if "Login :: Damn Vulnerable Web Application" in response.text:
        return False

    return True


def find_forms(url, session):
    """
    Fetch all forms from a webpage.
    """
    response = session.get(url, timeout=5)
    print("Final URL:", response.url)
    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")  
    print("Forms found:", len(forms))
    return forms


def get_form_details(form):
    """
    Extract method, action and input fields.
    """
    details = {}

    details["action"] = form.get("action")

    details["method"] = form.get("method", "get").lower()

    inputs = []

    for input_tag in form.find_all("input"):
        
        inputs.append({
            "type": input_tag.get("type"),
            "name": input_tag.get("name"),
            "value": input_tag.get("value", "")
        })

    details["inputs"] = inputs

    return details


def scan_sql(url, session):
    
    print("Scanning URL:", url)

    results = []

    try:

        forms = find_forms(url, session)
        
        if not forms:
            return results

        for form in forms:

            details = get_form_details(form)
            
            sql_fields = [
                "id",
                "user",
                "username",
                "search",
                "name",
                "query"
            ]


            has_sql_field = False

            for field in details["inputs"]:
                if field["name"] in sql_fields:
                    has_sql_field = True


            if not has_sql_field:
                continue

            if details["action"] == "#":
                target = url
            else:
                target = urljoin(url, details["action"])

            normal_response = session.get(
                target,
                params={"id": "1"},
                timeout=5
            )

            page_url = url.lower()

            if "xss" in page_url:
                return []

            for payload in TEST_VALUES:

                data = {}

                for field in details["inputs"]:
    
                    name = field["name"]

                    if not name:
                        continue

                    # keep hidden token
                    if field["type"] == "hidden":
                        data[name] = field["value"]
                        continue


                    # submit button
                    if field["type"] == "submit":
                        data[name] = field["value"]
                        continue


                    # inject payload only into input fields
                    data[name] = payload


                if details["method"] == "post":
                    response = session.post(
                        target,
                        data=data,
                        timeout=5
                    )
                    
                else:
                    response = session.get(
                        target,
                        params=data,
                        timeout=5
                    )

                baseline = clean_response(
                    requests.get(
                        url,
                        cookies=session.cookies
                    ).text
                )

                page = response.text.lower()

                sql_found = False

                SQL_INDICATORS = [
                    "sql syntax",
                    "mysql",
                    "mysqli",
                    "database error",
                    "you have an error in your sql syntax",
                    "unknown column",
                    "quoted string not properly terminated",
                    "warning: mysql",
                    "warning: mysqli"
                ]

                if clean_response(response.text) != baseline:

                    for indicator in SQL_INDICATORS:
                        if indicator in page:
                            sql_found = True
                            break

                if sql_found:
                    if not results:
                        results.append({
                            "Form Action": target,
                            "Method": details["method"].upper(),
                            "Status": "Potential SQL Injection",
                            "Reason": "SQL-related response detected after payload"
                        })


                # DVWA style detection
                success_keywords = [
                    "first name",
                    "surname" 
                ]


                vulnerable = False
                for keyword in success_keywords:
                    if keyword in page:
                        vulnerable = True
                        break

                if vulnerable:
                    results.append({
                        "Form Action": target,
                        "Method": details["method"].upper(),
                        "Status": "Potential SQL Injection",
                        "Reason": "Response changed after SQL payload"
                    })
                    break
                    
                # Response difference detection
                if len(response.text) > len(normal_response.text) + 100:
                    results.append({
                        "Form Action": target,
                        "Method": details["method"].upper(),
                        "Status": "Potential SQL Injection",
                        "Reason": "Response changed after SQL payload"
                    })
                    break

        print("SQL RESULTS:", results)
        
        return results


    except requests.exceptions.Timeout:
        return [{"Error": "Request timed out while scanning the target."}]

    except requests.exceptions.RequestException as e:
        return [{"Error": str(e)}]