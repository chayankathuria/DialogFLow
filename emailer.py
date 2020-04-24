#import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config_reader import ConfigReader
#import pandas as pd
#import csv
class EmailSender:
    def send_email_to_student(self, recepient_email,message):

        self.config_reader=ConfigReader()
        self.configuration=self.config_reader.read_config()
        host = 'smtp.gmail.com'
        port = 587 
    
        message = MIMEMultipart()
        
        self.msg['From'] = self.configuration['SENDER_EMAIL']

        # storing the receivers email address
        self.msg['To'] = ",".join(recepient_email)

        # storing the subject
        self.msg['Subject'] = self.configuration['EMAIL_SUBJECT']
        
        #message['To'] = "chayands88@gmail.com"
        #message['From'] = "chayankathuria@gmail.com"
        #message['subject'] = "Test01"
        #message['Password']='ck@gmail80'
        body = "Hi You just ordered a Pizza from PizzaBot by Chayan!"
        html_body = MIMEText(body, 'plain')
        message.attach(html_body)
        username = "chayankathuria"
        passw = 'ck@gmail80'
        conn = smtplib.SMTP(host, port)
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
        conn.login(username,passw)    
        conn.sendmail('chayankathuria@gmail.com',self.msg['To'],message.as_string())
        #conn.sendmail(user, receiver, message.as_string())
        conn.quit()