import socket

COMMON_PORTS = {

    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP Alt"

}


def scan_ports(host):

    open_ports = []


    for port, name in COMMON_PORTS.items():

        try:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            s.settimeout(1)

            result = s.connect_ex(
                (host, port)
            )


            # Only add if connection succeeds
            if result == 0:

                if port in [21, 23, 3306]:
                    risk = "High"

                elif port in [22, 80, 443]:
                    risk = "Low"

                else:
                    risk = "Medium"


                open_ports.append({
                    "Port": port,
                    "Service": name,
                    "Risk": risk
                })


            s.close()


        except socket.error:
            continue


    return open_ports