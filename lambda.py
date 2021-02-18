import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from generate_report import create_analytics_report
import environ
import boto3

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
        

#def lambda_handler(event, context):
def lambda_handler():
    # Production variables
    # EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    # EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    # Development variables
    EMAIL_ADDRESS = env('EMAIL_ADDRESS')
    EMAIL_PASSWORD = env('EMAIL_PASSWORD')
    get_s3 = boto3.client('s3')
    S3_Bucket = env('S3_BUCKET')
    
    msg = EmailMessage()
    msg['Subject'] = 'TEST from Lambda Safelite Ticket Overview for SD'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ['holly.robertson@safelite.com']
    
    today = (datetime.now()).strftime("%m/%d/%y").replace("/0", "/").lstrip("0")
    
    new_filename = create_analytics_report(today, filename=f"cherwell_tickets_report.pdf")
    
    obj = get_s3.get_object(Bucket=S3_Bucket, Key=new_filename)
    contents = obj['Body'].read()
    msg.set_content('Attached is the daily analytics report for the Safelite Service Delivery Team.')
    msg.add_attachment(contents, filename=new_filename, maintype='application/pdf', subtype='html')
    
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
