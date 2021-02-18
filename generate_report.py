# Python libraries
from fpdf import FPDF
from datetime import datetime, timedelta
import os
from format_charts import plot_data
import environ
import boto3
from botocore.exceptions import NoCredentialsError

# Height and Width of pdf page
WIDTH = 210
HEIGHT = 297

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
        
def upload_to_aws(pdf, new_filename):
    # Production variables
    #ACCESS_KEY = os.environ.get('ACCESS_KEY')
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Development variables
    #ACCESS_KEY = env('ACCESS_KEY')
    #SECRET_KEY = env('SECRET_KEY')
    S3_Bucket = env('S3_BUCKET')
    s3 = boto3.client('s3')

    try:
      with open(f"tmp/{new_filename}", "rb") as f:
      #  with open(f"/tmp/{new_filename}", "rb") as f:
          s3.upload_fileobj(f, S3_Bucket, new_filename)
      print("Upload to S3 Successful")
      return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print("Error in Uploading ", e)
        return False


def create_title(today, pdf):
  ''' First Page '''
  pdf.add_page()
  pdf.image("./resources/letterhead_cropped.png", 0, 0, WIDTH)
  # Unicode is not yet supported in the py3k version; use windows-1252 standard font
  pdf.set_font('Courier', '', 24)  
  pdf.ln(40)
  pdf.write(5, "Cherwell Analytics Report")
  pdf.ln(10)
  pdf.set_font('Courier', '', 16)
  pdf.write(4, f'{today}')
  pdf.ln(5)

def create_analytics_report(today, filename="cherwell_tickets_report.pdf"):
  # Set Page Size
  pdf = FPDF() # A4 (210 by 297 mm)

  plot_data(today)
  create_title(today, pdf)
  pdf.image("tmp/ITSD_Chart.png", 1, 70, WIDTH/2)
  pdf.image("tmp/CCSD_Chart.png", 111, 70, WIDTH/2)
  pdf.image("tmp/ITSD_72_Chart.png", 1, 160, WIDTH/2)
  pdf.image("tmp/CCSD_72_Chart.png", 111, 160, WIDTH/2)


  ''' Second Page '''
  create_title(today, pdf)
  pdf.image("tmp/SD_7_Chart.png", 1, 70, WIDTH/2)
  pdf.image("tmp/SD_30_Chart.png", 111, 70, WIDTH/2)


  formatted_today = today.replace("/", "-")
  new_filename =  formatted_today + "_" + filename
  try:
    pdf.output("tmp/" + new_filename, 'F')
    #pdf.output("/tmp/" + new_filename, 'F')
    upload_to_aws(pdf, new_filename)
  except Exception as e:
    print('Error in output', str(e), '******')

  return new_filename
  
if __name__ == '__main__':
  today = (datetime.today()).strftime("%m/%d/%y").replace("/0","/").lstrip("0")

  create_analytics_report(today)
