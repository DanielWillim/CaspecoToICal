import tabula
import pandas
import numpy as np
import icalendar as ical
from icalendar import Calendar, Event
from datetime import datetime
from dateutil import parser

#read file
file = "data.pdf"
df = tabula.read_pdf(file, pages='all')

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

f = open('Output/harryda.ics', 'wb')
f.write(cal.to_ical())
f.close()