import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
def sendEmail(subject,sender,reciver,text):
    mail = Mail(sender, subject, reciver, text)
