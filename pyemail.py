import smtplib

from email.mime.text import MIMEText


msg = MIMEText("afdasfdasfdsfdasfds")
msg['Subject'] = 'The Subject'
msg['From'] = "checker"
msg['To'] = "chris"

s = smtplib.SMTP('mail.zzzz.net')
fromm = "chris@zzz.com"
too = "chris@zzz.com"
s.sendmail(fromm, too , msg.as_string())
s.quit()



