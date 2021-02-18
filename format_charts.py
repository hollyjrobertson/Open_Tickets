from datetime import datetime
import plotly.graph_objects as g
import os
from helper import getCCSDTickets, getITSDTickets, getCCSD72Tickets, getITSD72Tickets, getSD_7CatList, getSD_30CatList

def format_lists():
    it_names, it_72, it_values, it_72_values = [], [], [], []
    cc_names, cc_72, cc_values, cc_72_values = [], [], [], []
    sd_30_cats, sd_30_values, sd_7_cats, sd_7_values = [], [], [], []
    
    for i in getITSDTickets():
        it_names.append(i[0])
        it_values.append(i[1])
    
    for h in getITSD72Tickets():
        it_72.append(h[0])
        it_72_values.append(h[1])
    
    for j in getCCSDTickets():
        cc_names.append(j[0])
        cc_values.append(j[1])

    for k in getCCSD72Tickets():
        cc_72.append(k[0])
        cc_72_values.append(k[1])
    
    for a in getSD_7CatList():
        sd_7_cats.append(a[0])
        sd_7_values.append(a[1])
    
    for b in getSD_30CatList():
        sd_30_cats.append(b[0])
        sd_30_values.append(b[1])
    
    setITSDNames(it_names)
    setITSDValues(it_values)
    setSD_7_Categories(sd_7_cats)
    setSD_7_CatValues(sd_7_values)
    setSD_30_Categories(sd_30_cats)
    setSD_30_CatValues(sd_30_values)
    setITSD72Names(it_72)
    setITSD72Values(it_72_values)
    setCCSDNames(cc_names)
    setCCSDValues(cc_values)
    setCCSD72Names(cc_72)
    setCCSD72Values(cc_72_values)

def setITSD72Names(it_72):
    global ITSD_72_Names
    if it_72:
        ITSD_72_Names = it_72
    else:
        ITSD_72_Names = None
        
def setITSD72Values(it_72_values):
    global ITSD_72_Values
    if it_72_values:
        ITSD_72_Values = it_72_values
    else:
        ITSD_72_Values = None
        
def setCCSD72Names(cc_72):
    global CCSD_72_Names
    if cc_72:
        CCSD_72_Names= cc_72
    else:
        CCSD_72_Names = None
        
def setCCSD72Values(cc_72_values):
    global CCSD_72_Values
    if cc_72_values:
        CCSD_72_Values = cc_72_values
    else:
        CCSD_72_Values = None

def setSD_7_Categories(sd_7_cats):
    global SD_7_Cats
    
    if sd_7_cats:
        SD_7_Cats = sd_7_cats
    else:
        SD_7_Cats = None

def setSD_7_CatValues(sd_7_values):
    global SD_7_CatValues
    if sd_7_values:
        SD_7_CatValues = sd_7_values
    else:
        SD_7_CatValues = None

def setSD_30_Categories(sd_30_cats):   
    global SD_30_Cats
    if sd_30_cats:
        SD_30_Cats = sd_30_cats
    else:
        SD_30_Cats = None

def setSD_30_CatValues(sd_30_values):
    global SD_30_CatValues
    if sd_30_values:
        SD_30_CatValues = sd_30_values
    else:
        SD_30_CatValues = None

def setCCSDNames(cc_names):
    global CCSD_Names
    if cc_names:
        CCSD_Names = cc_names
    else:
        CCSD_Names = None

def setCCSDValues(cc_values):
    global CCSD_Values
    if cc_values:
        CCSD_Values = cc_values
    else:
        CCSD_Values = None

def setITSDNames(names):
    global ITSD_Names
    if names:
        ITSD_Names = names
    else:
        ITSD_Names = None
        
def setITSDValues(values):
    global ITSD_Values
    
    if values:
        ITSD_Values = values
    else:
        ITSD_Values = None
        
def getITSDNames():
    try:
        ITSD_Names
    except: 
        format_lists()
        
    return ITSD_Names

def getITSDValues():
    try:
        ITSD_Values
    except: 
        format_lists()
    
    return ITSD_Values

def getSD_7_Categories():
    try:
        SD_7_Cats
    except:
        format_lists()
    
    return SD_7_Cats

def getSD_7_CatValues():
    try:
        SD_7_CatValues
    except:
        format_lists()
    
    return SD_7_CatValues

def getSD_30_Categories():
    try:
        SD_30_Cats
    except:
        format_lists()
    
    return SD_30_Cats

def getSD_30_CatValues():
    try:
        SD_30_CatValues
    except:
        format_lists()
    
    return SD_30_CatValues

def getITSD72Names():
    try:
        ITSD_72_Names
    except:
        format_lists()
    
    return ITSD_72_Names

def getITSD72Values():
    try:
        ITSD_72_Values
    except:
        format_lists()
        
    return ITSD_72_Values
        
def getCCSD72Names():
    try:
        CCSD_72_Names
    except:
        format_lists()
        
    return CCSD_72_Names

def getCCSD72Values():
    try:
        CCSD_72_Values
    except:
        format_lists()
    
    return CCSD_72_Values
        
def getCCSDValues():
    try:
        CCSD_Values
    except:
        format_lists()
    
    return CCSD_Values

def getCCSDNames():
    try:
        CCSD_Names
    except:
        format_lists()
    
    return CCSD_Names

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
    #fig.show()