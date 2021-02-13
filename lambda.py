import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from generate_report import create_analytics_report
import environ

#def lambda_handler(event, context):
def lambda_handler():
    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False)
    )
    # reading .env file
    environ.Env.read_env()
    
    # EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    # EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    EMAIL_ADDRESS = env('EMAIL_ADDRESS')
    EMAIL_PASSWORD = env('EMAIL_PASSWORD')
    
    msg = EmailMessage()
    msg['Subject'] = 'Safelite Ticket Overview for SD'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ['holly.robertson@safelite.com']
    
    msg.set_content('Attached is the report of all open Cherwell tickets for the Safelite Service Delivery Team.')

    today = (datetime.now()).strftime("%m/%d/%y").replace("/0", "/").lstrip("0")

    create_analytics_report(today, filename=f"cherwell_tickets_report.pdf")
    
    with open(f'cherwell_tickets_report.pdf', 'rb') as f:
        data = f.read()
        
    msg.add_attachment(data, filename='cherwell_tickets_report.pdf', maintype='application/pdf', subtype='pdf')
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            try:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                print("Successfully Logged-in")
            except Exception as e:
                print('Error within Logging In', str(e))
            
            try:
                smtp.send_message(msg)
                print("Message Sent Successfully")
            except Exception as f:
                print('Error with sending email', str(f))
    except Exception as h:
        print('Error with WITH', str(h))
        

lambda_handler()