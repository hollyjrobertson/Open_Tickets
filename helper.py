import pandas as pd
import environ
import requests
import collections

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
    
def load_relevant_data():
    url = env('PROD_CHERWELL_API') + "api/V1/getsearchresults/association/" + env('Incident_bus_obj_id')  + "scope/Global/scopeowner/(None)/searchname/" + env('SEARCH_OPEN_SD_TICKETS')

    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getBToken(),
        'Cookie': env('CHERWELL_COOKIE')
    }
    
    if btoken != None:
        response = requests.request("GET", url, headers=headers, data=payload)
        total_tickets = formatResponse(response)
    else:
        total_tickets = None
    return total_tickets 

def setBtoken():
    global btoken
    
    url = env('PROD_CHERWELL_API') + "token"

    payload='auth_mode=' + env('AUTH_MODE') + '&grant_type=' + env('GRANT_TYPE') + '&client_id=' + env('CHERWELL_CLIENT_ID') + '&username=' + env('CHERWELL_USERNAME') + '&password=' + env('CHERWELL_PWD')
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + env('CHERWELL_BEARER'),
    'Cookie': env('CHERWELL_COOKIE')
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code != 400:
        btoken = response.json()['access_token'] 
    else:
        btoken = None
    
    return btoken

def getBToken():
    try:
        btoken
    except:
        setBtoken()
    
    return btoken

def formatResponse(response):
    aged_ticket_list = []
    total = len(response.json()['businessObjects'])
    i = 0
    total_tickets = 1
    while i < total:
        employee = response.json()['businessObjects'][i]['fields'][7]['value']
        ticket = response.json()['businessObjects'][i]['fields'][1]['value'] 
        created = response.json()['businessObjects'][i]['fields'][3]['value']
        team = response.json()['businessObjects'][i]['fields'][6]['value']   
        aged_ticket_list.append(
            {
                'Total' : total_tickets,
                'Ticket': ticket, 
                'Created': created, 
                'Team': team,
                'Employee': employee,
            }
        )
        
        i += 1
        
    format_aged_ticket_list(aged_ticket_list)
    
    return len(aged_ticket_list)

def format_aged_ticket_list(list):
    temp_cc_aged_ticket_list = []
    temp_it_aged_ticket_list = []
    cc_aged_ticket_list = []
    it_aged_ticket_list = []
    cc_counter = collections.Counter()
    it_counter = collections.Counter()
    
    for employee in list:
        if (employee['Team'] == 'Call Center Service Desk'):
            temp_cc_aged_ticket_list.append(employee)
        else:
            temp_it_aged_ticket_list.append(employee)
    
    for x in temp_cc_aged_ticket_list:
        name = x['Employee']
        cc_counter.update({name})
    
    for y in temp_it_aged_ticket_list:
        name = y['Employee']
        it_counter.update({name})   

    for m in cc_counter.items():
        cc_aged_ticket_list.append(m)
    
    for x in it_counter.items():
        it_aged_ticket_list.append(x)
    
    it_aged_ticket_list.sort(reverse=False, key=lambda employee: employee[1])
    cc_aged_ticket_list.sort(reverse=False, key=lambda employee: employee[1])

    setTicketLists(cc_aged_ticket_list, it_aged_ticket_list)

def setTicketLists(cc_aged_ticket_list, it_aged_ticket_list):
    global it_aged_ticket_totals
    global cc_aged_ticket_totals
    
    if it_aged_ticket_list:
        if cc_aged_ticket_list:
            it_aged_ticket_totals = it_aged_ticket_list
            cc_aged_ticket_totals = cc_aged_ticket_list
    elif it_aged_ticket_list:
        it_aged_ticket_totals = it_aged_ticket_list
    elif cc_aged_ticket_list:
        cc_aged_ticket_totals = cc_aged_ticket_list
    else:
        it_aged_ticket_totals = None
        cc_aged_ticket_totals = None

def getCCSDTickets():
    try:
        cc_aged_ticket_totals
    except:
        load_relevant_data()
    
    return cc_aged_ticket_totals
        
def getITSDTickets():
    try:
        it_aged_ticket_totals
    except:
        load_relevant_data()
    
    return it_aged_ticket_totals





	# # This can be changed to your local directory (./) for testing purposes
	# BASE_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
	# #BASE_PATH = './data/'
	# if us_data and mode == Mode.CASES:
	# 	PATH = BASE_PATH + 'time_series_covid19_confirmed_US.csv'
	# elif us_data and mode == Mode.DEATHS:
	# 	PATH = BASE_PATH + 'time_series_covid19_deaths_US.csv'
	# elif not us_data and mode == Mode.CASES:
	# 	PATH = BASE_PATH + 'time_series_covid19_confirmed_global.csv'
	# elif not us_data and mode == Mode.DEATHS:
	# 	PATH = BASE_PATH + 'time_series_covid19_deaths_global.csv'

	# return pd.read_csv(PATH)

def get_state_names():
    df = load_relevant_data()
    return df['Province_State'].unique()

def get_country_names():
    df = load_relevant_data(us_data=False)
    return df['Country/Region'].unique()

# # United States of America Python Dictionary to translate States,
# # Districts & Territories to Two-Letter codes and vice versa.
# #
# # https://gist.github.com/rogerallen/1583593
# #
# # Dedicated to the public domain.  To the extent possible under law,
# # Roger Allen has waived all copyright and related or neighboring
# # rights to this code.

# us_state_abbrev = {
#     'Alabama': 'AL',
#     'Alaska': 'AK',
#     'American Samoa': 'AS',
#     'Arizona': 'AZ',
#     'Arkansas': 'AR',
#     'California': 'CA',
#     'Colorado': 'CO',
#     'Connecticut': 'CT',
#     'Delaware': 'DE',
#     'District of Columbia': 'DC',
#     'Florida': 'FL',
#     'Georgia': 'GA',
#     'Guam': 'GU',
#     'Hawaii': 'HI',
#     'Idaho': 'ID',
#     'Illinois': 'IL',
#     'Indiana': 'IN',
#     'Iowa': 'IA',
#     'Kansas': 'KS',
#     'Kentucky': 'KY',
#     'Louisiana': 'LA',
#     'Maine': 'ME',
#     'Maryland': 'MD',
#     'Massachusetts': 'MA',
#     'Michigan': 'MI',
#     'Minnesota': 'MN',
#     'Mississippi': 'MS',
#     'Missouri': 'MO',
#     'Montana': 'MT',
#     'Nebraska': 'NE',
#     'Nevada': 'NV',
#     'New Hampshire': 'NH',
#     'New Jersey': 'NJ',
#     'New Mexico': 'NM',
#     'New York': 'NY',
#     'North Carolina': 'NC',
#     'North Dakota': 'ND',
#     'Northern Mariana Islands':'MP',
#     'Ohio': 'OH',
#     'Oklahoma': 'OK',
#     'Oregon': 'OR',
#     'Pennsylvania': 'PA',
#     'Puerto Rico': 'PR',
#     'Rhode Island': 'RI',
#     'South Carolina': 'SC',
#     'South Dakota': 'SD',
#     'Tennessee': 'TN',
#     'Texas': 'TX',
#     'Utah': 'UT',
#     'Vermont': 'VT',
#     'Virgin Islands': 'VI',
#     'Virginia': 'VA',
#     'Washington': 'WA',
#     'West Virginia': 'WV',
#     'Wisconsin': 'WI',
#     'Wyoming': 'WY'
# }

# # thank you to @kinghelix and @trevormarburger for this idea
# abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

# # Simple test examples
# if __name__ == '__main__':
#     print("Wisconin --> WI?", us_state_abbrev['Wisconsin'] == 'WI')
#     print("WI --> Wisconin?", abbrev_us_state['WI'] == 'Wisconsin')
#     print("Number of entries (50 states, DC, 5 Territories) == 56? ", 56 == len(us_state_abbrev))

