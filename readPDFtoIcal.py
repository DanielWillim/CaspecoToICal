from pprint import pprint
from tabula import read_pdf
import pandas
import numpy as np
import icalendar as ical
from icalendar import Calendar, Event
from datetime import datetime
from dateutil import parser

def caspecoToCal(inPath, outPath):
    #read file

    df = read_pdf(inPath, pages='all')

    data = df[0].values

    for i in range(1, len(df)):
        data = np.concatenate((data, [df[i].columns.tolist()], df[i].values), axis=0)

    data = data[:-1]

    #Create calendar
    cal = Calendar()

    for curr in data:
        event = Event()
        event.add('summary', curr[0] + " - " + curr[1])
        event.add('dtstart', parser.parse(curr[2]))
        event.add('dtend', parser.parse(curr[3]))

        cal.add_component(event)

    f = open(outPath, 'wb')
    f.write(cal.to_ical())
    f.close()

caspecoToCal("summer2022/Bokningsläge Härryda.pdf", "Output/härryda.ics")
caspecoToCal("summer2022/Bokningsläge JV.pdf", "Output/jvg.ics")
caspecoToCal("summer2022/Bokningsläge KG.pdf", "Output/kg.ics")