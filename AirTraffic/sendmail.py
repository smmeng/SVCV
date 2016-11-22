#http://naelshiab.com/tutorial-send-email-python/
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
fromaddr = "redbiglobster@gmail.com"
toaddr = "smmeng@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Flight DataFeed Crashed!"
 
body = "Please rescue me!"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "gong0425")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()