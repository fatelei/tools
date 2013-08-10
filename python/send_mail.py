#!/usr/bin/env python
#-*-coding: utf8-*-

import smtplib
import argparse

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(to):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = u'test'
    msg['From'] = u'fatedes@163.com'
    msg['To'] = "to"
    content = """
        <html>
            <body>
                <p>testy</p>
            </body>
        </html>
    """
    html = MIMEText(content, "html")
    msg.attach(html)
    s = smtplib.SMTP("smtp.163.com")
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("fatedes@163.com", "k7yeq&fate")
    s.sendmail("fatedes@163.com", [to], msg.as_string())
    s.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="send email")
    parser.add_argument("-t", dest="to", type=str, help="email address")
    args = parser.parse_args()
    if args.to:
        send_mail(to)