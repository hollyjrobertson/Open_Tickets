import plotly.graph_objects as g
import os
from helper import getCCSDTickets, getITSDTickets

def format_lists():
    names = []
    values = []
    for i in getITSDTickets():
        names.append(i[0])
        values.append(i[1])

    setITSDNames(names)
    setITSDValues(values)
    
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

def plot_data():
    x = getITSDValues()
    y = getITSDNames()
    
    fig = g.Figure(
        data = [
            g.Bar(
                x = x,
                y = y, 
                orientation = 'h'
            )
        ]
    )
    
    fig.write_image('tmp/ITSD_Chart.png')
    