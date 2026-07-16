from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(filename, data):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []


    content.append(
        Paragraph(
            "Mini Penetration Testing Toolkit Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))


    # Target URL
    content.append(
        Paragraph(
            f"Target URL: {data.get('url')}",
            styles["Normal"]
        )
    )


    content.append(Spacer(1, 15))


    # Risk Score

    risk = data.get("risk")


    content.append(
        Paragraph(
            "Security Risk Assessment",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
            f"Risk Score: {risk['score']}/100",
            styles["Normal"]
        )
    )


    content.append(
        Paragraph(
            f"Risk Level: {risk['level']}",
            styles["Normal"]
        )
    )


    content.append(Spacer(1,15))


    # Issues

    content.append(
        Paragraph(
            "Detected Issues:",
            styles["Heading2"]
        )
    )


    for issue in risk["issues"]:

        content.append(
            Paragraph(
                "- " + issue,
                styles["Normal"]
            )
        )


    content.append(Spacer(1,20))


    # SQL Results

    content.append(
        Paragraph(
            "SQL Injection Scan:",
            styles["Heading2"]
        )
    )


    if data["sql_result"]:

        for item in data["sql_result"]:

            content.append(
                Paragraph(
                    str(item),
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No SQL Injection detected",
                styles["Normal"]
            )
        )



    content.append(Spacer(1,20))


    # XSS

    content.append(
        Paragraph(
            "XSS Scan:",
            styles["Heading2"]
        )
    )


    if data["xss_result"]:

        for item in data["xss_result"]:

            content.append(
                Paragraph(
                    str(item),
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No XSS indicators detected",
                styles["Normal"]
            )
        )



    content.append(Spacer(1,20))


    # SSL

    content.append(
        Paragraph(
            "SSL Analysis:",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
            str(data["ssl_result"]),
            styles["Normal"]
        )
    )


    pdf.build(content)