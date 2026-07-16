import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def login_to_dvwa(session, base_url="http://localhost/dvwa/"):

    login_url = urljoin(base_url, "login.php")

    # Get login page
    response = session.get(login_url)

    soup = BeautifulSoup(response.text, "html.parser")

    token = soup.find("input", {"name": "user_token"})

    user_token = token["value"] if token else ""

    login_data = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": user_token
    }

    response = session.post(login_url, data=login_data)

    if "Login :: Damn Vulnerable Web Application" in response.text:
        print("Login Failed")
        return False

    print("Login Successful")

    # -----------------------------
    # Set DVWA Security = Low
    # -----------------------------
    security_url = urljoin(base_url, "security.php")

    response = session.get(security_url)

    soup = BeautifulSoup(response.text, "html.parser")

    token = soup.find("input", {"name": "user_token"})

    user_token = token["value"] if token else ""

    security_data = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": user_token
    }

    session.post(security_url, data=security_data)

    print("Security set to LOW")

    print("Cookies:", session.cookies.get_dict())

    return True
