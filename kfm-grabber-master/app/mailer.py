# -*- coding: utf-8 -*-

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.utils import formatdate
# from email.mime.text import MIMEText
# from app.creds import Mail
#
# #Function wooppay smtp sender
# def wooppay_smtp(subject, text, smtp_list):
#     """
#
#     :param subject: Message theme
#     :param text: Message data
#     :param smtp_list: list recipients
#     :return:
#     """
#     msg = MIMEMultipart()
#     msg['From'] = Mail.smtp_from_email
#     msg['To'] = ','.join(smtp_list)
#     msg['Date'] = formatdate(localtime=True)
#     msg['Subject'] = subject
#     text = text
#     part = MIMEText(text, 'plain')
#     msg.attach(part)
#     try:
#         server = smtplib.SMTP(Mail.smtp_server, Mail.smtp_port)
#         server.ehlo("mail.wooppay.com")
#         server.starttls()
#         server.ehlo("mail.wooppay.com")
#         server.docmd('auth login')
#         server.docmd(Mail.smtp_b64_username)
#         server.docmd(Mail.smtp_b64_password)
#         server.sendmail(Mail.smtp_username, smtp_list, msg.as_string())
#         server.quit()
#     except Exception as e:
#         pass