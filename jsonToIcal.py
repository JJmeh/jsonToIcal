#!/usr/bin/python3

import json
from datetime import datetime
from icalendar import Calendar, Event, vDatetime
import uuid
import pytz
import tempfile, os
import sys, getopt

ifile = ''
ofile = ''
myopts, args = getopt.getopt(sys.argv[1:], "i:o:")

for o, a in myopts:
    if o == '-i':
        ifile = a
    elif o == '-o':
        ofile = a
    else:
        print("Usage: %s -i data.json -o calendar.ics" % sys.argv[0])

f = open(ifile, 'r')
# print(f)
data = json.load(f)

numOfJsonItem = len(data) # count number of json data

timeStamp = datetime.today()
# print(timeStamp)
cal = Calendar()

cal.add('version', '1.0')
cal.add('prodid', '-//Test//meh.com//')
cal.add('name', 'test event')

def timeCreate(time, date):
    tm = time.split(':')
    hour = int(tm[0])
    minute = int(tm[1])
    dt = date.split(' ')[0].split('-')
    year = int(dt[0])
    month = int(dt[1])
    day = int(dt[2])
    return datetime(year, month, day, hour, minute, tzinfo=pytz.timezone('asia/jakarta'))

def getTitle(item):
    cType = item['N_DELIVERY_MODE']
    time = item['MEETING_TIME_START'].split(':')[0]
    if cType == 'GSLC':
        return '[' + cType + '] - ' + item['COURSE_TITLE_LONG'] + ' (' + item['CLASS_SECTION'] + ' | ' + item['CRSE_CODE'] + ')'
    else:
        if int(time) >= 12:
            return '{' + cType + '} - ' + item['COURSE_TITLE_LONG'] + ' (' + item['CLASS_SECTION'] + ' | ' + item['CRSE_CODE'] + ')'
        else:
            return '(' + cType + ') - ' + item['COURSE_TITLE_LONG'] + ' (' + item['CLASS_SECTION'] + ' | ' + item['CRSE_CODE'] + ')'

for i in range(0, numOfJsonItem):
    event = Event()

    item = data[i]
    # title : [GSLC] - Data Structure (LA02 / COMP6048)
    title = getTitle(item)

    id = str(uuid.uuid4()).split('-')[0] + '@https://binusmaya.binus.ac.id'
    event.add('uid', id)
    event.add('sequence', '0')
    event.add('dtstamp', timeStamp)
    event.add('dtstart', timeCreate(item['MEETING_TIME_START'], item['START_DT']))
    event.add('dtend', timeCreate(item['MEETING_TIME_END'], item['END_DT']))
    event.add('summary', title)
    event.add('description', item['COURSE_TITLE_LONG'] + ' ' + item['SSR_DESCR'])
    cal.add_component(event)

# print(cal.to_ical())

f1 = open(ofile, 'wb')
f1.write(cal.to_ical())

f1.close()
f.close()