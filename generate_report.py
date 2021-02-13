# Python libraries
from fpdf import FPDF
from datetime import datetime, timedelta
import os

# Local libraries
from format_charts import plot_data
#from daily_counts import plot_daily_count_states, plot_daily_count_countries
#from create_case_maps import plot_usa_case_map, plot_global_case_map
#from helper import Mode

WIDTH = 210
HEIGHT = 297

def create_title(day, pdf):
  # Unicode is not yet supported in the py3k version; use windows-1252 standard font
  pdf.set_font('Arial', '', 24)  
  pdf.ln(60)
  pdf.write(5, f"Cherwell Analytics Report")
  pdf.ln(10)
  pdf.set_font('Arial', '', 16)
  pdf.write(4, f'{day}')
  pdf.ln(5)

def create_analytics_report(day, filename="cherwell_tickets_report.pdf"):
  pdf = FPDF() # A4 (210 by 297 mm)
  plot_data()
  #states = ['Texas', 'Ohio']
  
  ''' First Page '''
  pdf.add_page()
  pdf.image("./resources/letterhead_cropped.png", 0, 0, WIDTH)
  create_title(day, pdf)
  pdf.image("tmp/ITSD_Chart.png", 5, 90, WIDTH/2-10)

  #plot_usa_case_map("./tmp/usa_cases.png", day=day)
  #prev_days = 250
  #plot_states(states, days=prev_days, filename="./tmp/cases.png", end_date=day)
  #plot_states(states, days=prev_days, mode=Mode.DEATHS, filename="./tmp/deaths.png", end_date=day)

  # pdf.image("./tmp/usa_cases.png", 5, 90, WIDTH-20)
  # pdf.image("./tmp/cases.png", 5, 200, WIDTH/2-10)
  # pdf.image("./tmp/deaths.png", WIDTH/2, 200, WIDTH/2-10)

  ''' Second Page '''
  pdf.add_page()

  # plot_daily_count_states(states, day=day, filename="./tmp/cases_day.png")
  # plot_daily_count_states(states, day=day, mode=Mode.DEATHS, filename="./tmp/deaths_day.png")
  # pdf.image("./tmp/cases_day.png", 5, 20, WIDTH/2-10)
  # pdf.image("./tmp/deaths_day.png", WIDTH/2, 20, WIDTH/2-10)

  # prev_days = 7
  # plot_states(states, days=prev_days, filename="./tmp/cases2.png", end_date=day)
  # plot_states(states, days=prev_days, mode=Mode.DEATHS, filename="./tmp/deaths2.png", end_date=day)
  # pdf.image("./tmp/cases2.png", 5, 110, WIDTH/2-10)
  # pdf.image("./tmp/deaths2.png", WIDTH/2, 110, WIDTH/2-10)

  # prev_days = 30
  # plot_states(states, days=prev_days, filename="./tmp/cases3.png", end_date=day)
  # plot_states(states, days=prev_days, mode=Mode.DEATHS, filename="./tmp/deaths3.png", end_date=day)
  # pdf.image("./tmp/cases3.png", 5, 200, WIDTH/2-10)
  # pdf.image("./tmp/deaths3.png", WIDTH/2, 200, WIDTH/2-10)

  ''' Third Page '''
  pdf.add_page()

  # plot_global_case_map("./tmp/global_cases.png", day=day)

  # countries = ['US', 'India', 'Brazil']
  # prev_days = 7
  # plot_countries(countries, days=prev_days, filename="./tmp/cases4.png", end_date=day)
  # plot_countries(countries, days=prev_days, mode=Mode.DEATHS, filename="./tmp/deaths4.png", end_date=day)

  # pdf.image("./tmp/global_cases.png", 5, 20, WIDTH-20)
  # pdf.image("./tmp/cases4.png", 5, 130, WIDTH/2-10)
  # pdf.image("./tmp/deaths4.png", WIDTH/2, 130, WIDTH/2-10)

  pdf.output(filename, 'F')


if __name__ == '__main__':
  today = (datetime.today()).strftime("%m/%d/%y").replace("/0","/").lstrip("0")

  create_analytics_report(today)
