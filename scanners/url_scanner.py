import requests

SECURITY_HEADERS = [
    "X-Frame-Options",
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options"
]

def scan_url(url):

    result = {}

    try:

        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True
        )

        result["Status Code"] = response.status_code

        result["HTTPS"] = "Enabled ✅" if url.startswith("https://") else "Not Enabled ❌"

        result["Redirects"] = len(response.history)

        result["Server"] = response.headers.get(
            "Server",
            "Unknown"
        )

        missing = []

        for header in SECURITY_HEADERS:

            if header not in response.headers:

                missing.append(header)

        result["Missing Headers"] = ", ".join(missing) if missing else "None"

    except Exception as e:

        result["Error"] = str(e)

    return result