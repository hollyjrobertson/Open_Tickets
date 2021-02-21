from datetime import datetime
import plotly.graph_objects as g
import os
from helper import getCCSDTickets, getITSDTickets, getCCSD72Tickets, getITSD72Tickets, getSD_7CatList, getSD_30CatList

def format_list(list):
    names = []
    values = []
    
    try:
        for i in list:
            names.append(i[0])
            values.append(i[1])
    except TypeError as t:
        names = [0]
        values = [0]
        
    return names, values

def setITSDChart():
    global ITSD_Names
    global ITSD_Values
    ITSD_Names, ITSD_Values = format_list(getITSDTickets())  
        
def getITSDNames():
    try:
        ITSD_Names
    except: 
        setITSDChart()
        
    return ITSD_Names

def getITSDValues():
    try:
        ITSD_Values
    except: 
        setITSDChart()
        
    return ITSD_Values

def setCCSDChart():
    global CCSD_Names
    global CCSD_Values
    CCSD_Names, CCSD_Values = format_list(getCCSDTickets())
    
def getCCSDNames():
    try:
        CCSD_Names
    except: 
        setCCSDChart()
    
    return CCSD_Names

def getCCSDValues():
    try:
        CCSD_Values
    except: 
        setCCSDChart()

    return CCSD_Values

def setSD_7DayChart():
    global SD_7_Cats
    global SD_7_CatValues
    SD_7_Cats, SD_7_CatValues = format_list(getSD_7CatList())

def getSD_7_Categories():
    try:
        SD_7_Cats
    except: 
        setSD_7DayChart()
    
    return SD_7_Cats

def getSD_7_CatValues():
    try:
        SD_7_CatValues
    except: 
        setSD_7DayChart()

    return SD_7_CatValues

def setSD_30DayChart():
    global SD_30_Cats
    global SD_30_CatValues
    SD_30_Cats, SD_30_CatValues = format_list(getSD_30CatList())

def getSD_30_Categories():
    try:
        SD_30_Cats
    except: 
        setSD_30DayChart()
    
    return SD_30_Cats

def getSD_30_CatValues():
    try:
        SD_30_CatValues
    except: 
        setSD_30DayChart()

    return SD_30_CatValues

def setITSD_72DayChart():
    global ITSD_72_Names
    global ITSD_72_Values
    ITSD_72_Names, ITSD_72_Values = format_list(getITSD72Tickets())

def getITSD72Names():
    try:
        ITSD_72_Names
    except: 
        setITSD_72DayChart()
    
    return ITSD_72_Names

def getITSD72Values():
    try:
        ITSD_72_Values
    except: 
        setITSD_72DayChart()

    return ITSD_72_Values

def setCCSD_72DayChart():
    global CCSD_72_Names
    global CCSD_72_Values
    CCSD_72_Names, CCSD_72_Values = format_list(getCCSD72Tickets())

def getCCSD72Names():
    try:
        CCSD_72_Names
    except: 
        setCCSD_72DayChart()
    
    return CCSD_72_Names

def getCCSD72Values():
    try:
        CCSD_72_Values
    except: 
        setCCSD_72DayChart()

    return CCSD_72_Values

def plot_category_data():
    x_7 = getSD_7_CatValues()
    y_7 = getSD_7_Categories()
    
    x_30 = getSD_30_CatValues()
    y_30 = getSD_30_Categories()
    
    sd_7_fig = g.Figure(g.Bar(
        x =  x_7 ,
        y = y_7, 
        text =  x_7,
        textposition = 'auto',
        textangle = 0,
        insidetextanchor='start',
        orientation = 'h',
        marker=dict(
            color='#167CAC',
            line=dict(color='#125B7E')
        )
    ))
    
    sd_7_fig.update_layout(
        title_text=("Top SD Categories - Last 7 Days"),
        yaxis=dict(
            title='Categories',
        ),
        xaxis=dict(
            title='# of Tickets Opened',
        ),
        bargap=0.15,
    )
    
    sd_30_fig = g.Figure(g.Bar(
        x = x_30,
        y = y_30, 
        text =  x_30,
        textposition = 'auto',
        textangle = 0,
        insidetextanchor='start',
        orientation = 'h',
        marker=dict(
            color='#167CAC',
            line=dict(color='#125B7E')
        )
    ))
    
    sd_30_fig.update_layout(
        title_text=("Top SD Categories - Last 30 Days"),
        yaxis=dict(
            title='Categories',
        ),
        xaxis=dict(
            title='# of Tickets Opened',
        ),
        bargap=0.15,
    )
    
    sd_7_fig.write_image('tmp/SD_7_Chart.png', width=900, height=1500, scale=1)
    sd_30_fig.write_image('tmp/SD_30_Chart.png', width=900, height=1500, scale=1)
    
def plot_72_data(today):
    x_ITSD = getITSD72Values()
    y_ITSD = getITSD72Names()
    
    x_CCSD = getCCSD72Values()
    y_CCSD = getCCSD72Names()

    itsd72_fig = g.Figure(g.Bar(
        x = x_ITSD,
        y = y_ITSD, 
        text = x_ITSD,
        textposition = 'auto',
        textangle = 0,
        insidetextanchor='start',
        orientation = 'h',
        marker=dict(
            color='#167CAC',
            line=dict(color='#125B7E')
        )
    ))
    
    itsd72_fig.update_layout(
        title_text=("ITSD Tickets > 72 hours"),
        yaxis=dict(
            title='Specialists',
        ),
        xaxis=dict(
            title='# of Tickets',
        ),
        bargap=0.15,
    )
    
    ccsd72_fig = g.Figure(g.Bar(
        x = x_CCSD,
        y = y_CCSD, 
        text = x_CCSD,
        textposition = 'auto',
        insidetextanchor='start',
        textangle = 0,
        orientation = 'h',
        marker=dict(
            color='#098649',
            line=dict(color='#075F35')
        )
    ))
    
    ccsd72_fig.update_layout(
        title_text=("CCSD Tickets > 72 hours"),
        yaxis=dict(
            title='Specialists',
        ),
        xaxis=dict(
            title='# of Tickets',
        ),
        bargap=0.15,
    )
    
    itsd72_fig.write_image('tmp/ITSD_72_Chart.png', width=900, height=800, scale=1)
    ccsd72_fig.write_image('tmp/CCSD_72_Chart.png', width=900, height=800, scale=1)
    
def plot_data(today):
    x_ITSD = getITSDValues()
    y_ITSD = getITSDNames()
    
    x_CCSD = getCCSDValues()
    y_CCSD = getCCSDNames()
    
    itsd_fig = g.Figure(g.Bar(
        x = x_ITSD,
        y = y_ITSD, 
        text = x_ITSD,
        textposition = 'auto',
        textangle = 0,
        insidetextanchor='start',
        orientation = 'h',
        marker=dict(
            color='#167CAC',
            line=dict(color='#125B7E')
        )
    ))
    
    itsd_fig.update_layout(
        title_text=("ITSD Open Tickets as of " + today),
        yaxis=dict(
            title='Specialists',
        ),
        xaxis=dict(
            title='# of Open Tickets',
        ),
        bargap=0.15,
    )
    
    ccsd_fig = g.Figure(g.Bar(
        x = x_CCSD,
        y = y_CCSD, 
        text = x_CCSD,
        textposition = 'auto',
        insidetextanchor='start',
        textangle = 0,
        orientation = 'h',
        marker=dict(
            color='#098649',
            line=dict(color='#075F35')
        )
    ))
    
    ccsd_fig.update_layout(
        title_text=("CCSD Open Tickets as of " + today),
        yaxis=dict(
            title='Specialists',
        ),
        xaxis=dict(
            title='# of Open Tickets',
        ),
        bargap=0.15,
    )
    
    itsd_fig.write_image('tmp/ITSD_Chart.png', width=900, height=800, scale=1)
    ccsd_fig.write_image('tmp/CCSD_Chart.png', width=900, height=800)
    plot_72_data(today)
    plot_category_data()
