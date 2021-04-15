# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def sendEmail(email_sender, email_sender_password, email_recipient, subject, message, log_path):
	 
	try:
		# create message object instance
		msg = MIMEMultipart()
		 
		# setup the parameters of the message
		password = email_sender_password
		msg['From'] = email_sender
		msg['To'] = email_recipient
		msg['Subject'] = subject
		 
		# attach log to message body
		#msg.attach(MIMEText(file(log_path).read()))
		
		# add in the message body
		msg.attach(MIMEText(message, 'plain'))

		#create server
		server = smtplib.SMTP('smtp.gmail.com: 587')
		 
		server.starttls()
		 
		# Login Credentials for sending the mail
		server.login(msg['From'], password)
		 
		 
		# send the message via the server.
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		
		server.quit()
		
		print("successfully sent email to: " + msg['To'])
		
	except Exception as e:
		   print(e)
		   print("No se pudo enviar el email")

