import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime


def check_ssl(url):
    try:
        parsed = urlparse(url)

        # If user entered http://...
        if parsed.scheme != "https":
            return {
                "Status": "Not Enabled ❌",
                "Reason": "Website is using HTTP instead of HTTPS."
            }

        hostname = parsed.hostname
        port = parsed.port or 443

        context = ssl.create_default_context()

        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                cert = ssock.getpeercert()

        issuer = dict(x[0] for x in cert["issuer"])

        issued_by = issuer.get("organizationName") or issuer.get("commonName")

        expiry = datetime.strptime(
            cert["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        issued = datetime.strptime(
            cert["notBefore"],
            "%b %d %H:%M:%S %Y %Z"
        )

        days_left = (expiry - datetime.utcnow()).days

        return {
            "Status": "Valid ✅",
            "Issuer": issued_by,
            "Valid From": issued.strftime("%d-%m-%Y"),
            "Expires On": expiry.strftime("%d-%m-%Y"),
            "Days Remaining": days_left
        }

    except Exception:
        return {
            "Status": "Error ❌",
            "Reason": "SSL connection timed out."
        }