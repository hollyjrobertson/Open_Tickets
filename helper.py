import pandas as pd
import environ
import requests
import collections
import logging


logging.basicConfig(level=logging.DEBUG, filename='tmp/dailyReport.log', format='%(asctime)s %(levelname)s:%(message)s')

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

def pullCherwellData():
    sd_7_url = env('PROD_CHERWELL_API') + "api/V1/getsearchresults/association/" + env('Incident_bus_obj_id')  + "scope/Global/scopeowner/(None)/searchname/" + env('SD_7_CATS')
    sd_30_url = env('PROD_CHERWELL_API') + "api/V1/getsearchresults/association/" + env('Incident_bus_obj_id')  + "scope/Global/scopeowner/(None)/searchname/" + env('SD_30_CATS')
    it_url = env('PROD_CHERWELL_API') + "api/V1/getsearchresults/association/" + env('Incident_bus_obj_id')  + "scope/Global/scopeowner/(None)/searchname/" + env('ITSD_72')
    cc_url = env('PROD_CHERWELL_API') + "api/V1/getsearchresults/association/" + env('Incident_bus_obj_id')  + "scope/Global/scopeowner/(None)/searchname/" + env('CCSD_72')
    url = env('PROD_CHERWELL_API') + "api/V1/getsearchresults/association/" + env('Incident_bus_obj_id')  + "scope/Global/scopeowner/(None)/searchname/" + env('SEARCH_OPEN_SD_TICKETS')
    
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getBToken(),
        'Cookie': env('CHERWELL_COOKIE')
    }
    
    if btoken != None:
        try:
            SD_30CatList = (formatCherwellResponse(requests.request("GET", sd_30_url, headers=headers, data=payload)))
            SD_7CatList = (formatCherwellResponse(requests.request("GET", sd_7_url, headers=headers, data=payload)))
            ITSD_72List = (formatCherwellResponse(requests.request("GET", it_url, headers=headers, data=payload)))
            CCSD_72List  = (formatCherwellResponse(requests.request("GET", cc_url, headers=headers, data=payload)))
            SD_OpenList = (formatCherwellResponseLimited(requests.request("GET", url, headers=headers, data=payload)))
        except Exception as e:
            print('Error in pullCherwellData', e)
    else:
        print('Error in getting btoken')
    
    try:
        parse_CC_v_IT_list(SD_OpenList)
        setSD_30CatList(sortListsByCategory(SD_30CatList))
        setSD_7CatList(sortListsByCategory(SD_7CatList))
        setITSD72List(sortListsByEmployee(ITSD_72List))
        setCCSD72List(sortListsByEmployee(CCSD_72List))
    except Exception as e:
        print('Error in parsing/setting', e)


def setBtoken():
    global btoken
    
    url = env('PROD_CHERWELL_API') + "token"
    payload='auth_mode=' + env('AUTH_MODE') + '&grant_type=' + env('GRANT_TYPE') + '&client_id=' + env('CHERWELL_CLIENT_ID') + '&username=' + env('CHERWELL_USERNAME') + '&password=' + env('CHERWELL_PWD')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + env('CHERWELL_BEARER'),
        'Cookie': env('CHERWELL_COOKIE'),
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

def formatCherwellResponseLimited(response):
    ticket_list = []
    total = len(response.json()['businessObjects'])
    i = 0
    while i < total:
        ticket = response.json()['businessObjects'][i]['fields'][1]['value']  
        team = response.json()['businessObjects'][i]['fields'][6]['value']  
        employee = response.json()['businessObjects'][i]['fields'][7]['value']
        ticket_list.append(
            {
                'Ticket': ticket, 
                'Team': team,
                'Employee': employee,
            }
        )
        
        i += 1
    
    return ticket_list

def formatCherwellResponse(response):
    ticket_list = []
    total = len(response.json()['businessObjects'])
    i = 0
    while i < total:
        ticket = response.json()['businessObjects'][i]['fields'][1]['value']  
        cat = response.json()['businessObjects'][i]['fields'][4]['value'] 
        subcat = response.json()['businessObjects'][i]['fields'][5]['value'] 
        created = response.json()['businessObjects'][i]['fields'][14]['value']
        team = response.json()['businessObjects'][i]['fields'][16]['value']  
        employee = response.json()['businessObjects'][i]['fields'][17]['value']
        ticket_list.append(
            {
                'Ticket': ticket, 
                'Created': created, 
                'Category': cat,
                'Subcategory': subcat,
                'Team': team,
                'Employee': employee,
            }
        )
        
        i += 1
    
    return ticket_list

def parse_CC_v_IT_list(list):
    temp_cc_aged_ticket_list = []
    temp_it_aged_ticket_list = []
    cc_aged_ticket_list = []
    it_aged_ticket_list = []
    
    for employee in list:
        if (employee['Team'] == 'Call Center Service Desk'):
            temp_cc_aged_ticket_list.append(employee)
        elif (employee['Team'] == 'Service Desk'):
            temp_it_aged_ticket_list.append(employee)
    
    it_aged_ticket_list = sortListsByEmployee(temp_it_aged_ticket_list)
    cc_aged_ticket_list = sortListsByEmployee(temp_cc_aged_ticket_list)
    setTicketLists(cc_aged_ticket_list, it_aged_ticket_list)

def sortListsByCategory(list):
    ticket_list = []
    temp_counter = collections.Counter()
            
    for i in list:
        cat = i['Category']
        temp_counter.update({cat})

    for x in temp_counter.items():
        ticket_list.append(x) 
    
    ticket_list.sort(reverse=False, key=lambda cat: cat[1]) 
    return ticket_list

def sortListsByEmployee(list):
    ticket_list = []
    temp_counter = collections.Counter()
            
    for i in list:
        employee = i['Employee']
        temp_counter.update({employee})

    for x in temp_counter.items():
        ticket_list.append(x) 
    
    ticket_list.sort(reverse=False, key=lambda employee: employee[1]) 
    
    return ticket_list

def setCCSD72List(list):
    global cc_72_ticket_list_totals
    
    if list:
        cc_72_ticket_list_totals = list
    else:
        cc_72_ticket_list_totals = None

def setITSD72List(list):
    global it_72_ticket_list_totals

    if list:
        it_72_ticket_list_totals = list
    else:
        it_72_ticket_list_totals = None
        
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

def setSD_30CatList(list):
    global sd_30_cats
    
    if list:
        sd_30_cats = list
    else:
        sd_30_cats = None
    
def setSD_7CatList(list):
    global sd_7_cats

    if list:
        sd_7_cats = list
    else:
        sd_7_cats = None
        
def getSD_30CatList():
    try:
        sd_30_cats
    except:
        pullCherwellData()
        
    return sd_30_cats
    
def getSD_7CatList():
    try:
        sd_7_cats
    except:
        pullCherwellData()
        
    return sd_7_cats

def getCCSDTickets():
    try:
        cc_aged_ticket_totals
    except:
        pullCherwellData()
    
    return cc_aged_ticket_totals
        
def getITSDTickets():
    try:
        it_aged_ticket_totals
    except:
        pullCherwellData()
    
    return it_aged_ticket_totals

def getITSD72Tickets():
    try:
        it_72_ticket_list_totals
    except:
        pullCherwellData()
    
    return it_72_ticket_list_totals

def getCCSD72Tickets():
    try:
        cc_72_ticket_list_totals
    except:
        pullCherwellData()
    
    return cc_72_ticket_list_totals

