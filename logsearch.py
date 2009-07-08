# vim:fileencoding=utf-8

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#   Copyright (c) 2009 by Paweł Tomak <satherot (at) gmail (dot) com>


from xml.dom import minidom
from datetime import datetime
import optparse
import re

cred = "\033[01;31m"
cgreen = "\033[01;32m"
cyellow = "\033[01;33m"
cblue = "\033[01;34m"
cmagenta = "\033[01;35m"
ccyan = "\033[01;36m"
cwhite = "\033[01;37m"

curtime = datetime.now()

optparser = optparse.OptionParser()
optparser.add_option("-f", dest="filename", help="nayzwa pliku", metavar="FILE")
optparser.add_option("-d", dest="date", help="tylko ten dzien(wyklucza --db i --de)", default="all")
optparser.add_option("--db", dest="datebg", help="od tego dnia", default="all")
optparser.add_option("--de", dest="dateend", help="do tego dnia", default="all")
optparser.add_option("--tb", dest="timebg", help="od tej godziny", default="all")
optparser.add_option("--te", dest="timeend", help="do tej godziny", default="all")
optparser.add_option("--tfa", dest="timeforall", help="ograniczenie od-do dla czasu bedzie dla wszystkich dni z zakresu", action="store_true")
optparser.add_option("-s", dest="search", help="szukanie bez rozrozniania wielkosci liter", metavar="SEARCH STRING")
optparser.add_option("-S", dest="search2", help="szukanie z rozroznianiem wielkosci liter", metavar="SEARCH STRING")
(opts, args) = optparser.parse_args()

if not (opts.filename):
    print "Musisz podac plik\n"
    exit()

if(opts.date != "all"):
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    if not (r.match(opts.date)):
        print "Bledny format daty. Format: YYYY-MM-DD"
        exit()
    year = int(opts.date[0:4])
    month = int(opts.date[5:7])
    day = int(opts.date[8:10])
    if(year > int(curtime.year)):
        print "Bledny rok"
        exit()
    elif(month > int(curtime.month) and (month > 12 or month <= 0)):
        print "Bledny miesiac"
        exit()
    elif(day > int(curtime.day) and (day > 31 or day <= 0)):
        print "Bledny dzien"
        exit()
    opts.datebg = "all"
    opts.dateend = "all"
else:
    if(opts.datebg != "all"):
        r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
        if not (r.match(opts.datebg)):
            print "Bledny format daty. Format: YYYY-MM-DD"
            exit()
        yearbg = int(opts.datebg[0:4])
        monthbg = int(opts.datebg[5:7])
        daybg = int(opts.datebg[8:10])
        if(yearbg > int(curtime.year)):
            print "Bledny rok"
            exit()
        elif(monthbg > int(curtime.month) and (monthbg > 12 or monthbg <= 0)):
            print "Bledny miesiac"
            exit()
        elif(daybg > int(curtime.day) and (daybg > 31 or daybg <= 0)):
            print "Bledny dzien"
            exit()
    if(opts.dateend != "all"):
        r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
        if not (r.match(opts.dateend)):
            print "Bledny format daty. Format: YYYY-MM-DD"
            exit()
        yearend = int(opts.dateend[0:4])
        monthend = int(opts.dateend[5:7])
        dayend = int(opts.dateend[8:10])
        if(yearend > int(curtime.year)):
            print "Bledny rok"
            exit()
        elif(monthend > int(curtime.month) and (monthend > 12 or monthend <= 0)):
            print "Bledny miesiac"
            exit()
        elif(dayend > int(curtime.day) and (dayend > 31 or dayend <= 0)):
            print "Bledny dzien"
            exit()


if(opts.timebg != "all"):
    r = re.compile("[0-9]{2}:[0-9]{2}")
    if not (r.match(opts.timebg)):
        print "Bledny format czasu poczatkowego. Format: HH:MM"
        exit()
    hourbg = int(opts.timebg[0:2])
    minutebg = int(opts.timebg[3:5])
    if(hourbg < 0 or hourbg >= 24):
        print "Bledna godzina"
        exit()
    if(minutebg < 0 or minutebg >= 60):
        print "Bledne minuty"
        exit()
    if(opts.date == "all" and opts.datebg == "all"):
        yearbg = int(curtime.year)
        monthbg = int(curtime.month)
        daybg = int(curtime.day)

if(opts.timeend != "all"):
    r = re.compile("[0-9]{2}:[0-9]{2}")
    if not (r.match(opts.timeend)):
        print "Bledny format czasu poczatkowego. Format: HH:MM"
        exit()
    hourend = int(opts.timeend[0:2])
    minuteend = int(opts.timeend[3:5])
    if(hourend < 0 or hourend >= 24):
        print "Bledna godzina"
        exit()
    if(minuteend < 0 or minuteend >= 60):
        print "Bledne minuty"
        exit()
    if(opts.date == "all" and opts.dateend == "all"):
        yearend = int(curtime.year)
        monthend = int(curtime.month)
        dayend = int(curtime.day)

if opts.search:
    s = re.compile(opts.search, re.IGNORECASE)

if opts.search2:
    s = re.compile(opts.search2)

log = minidom.parse(opts.filename)
log = log.getElementsByTagName('message')

date = ""
pdate = ""

for i in range(0, log.length):
    time = log[i].getElementsByTagName('received')
    time = time[0].childNodes[0].nodeValue
    time = datetime.fromtimestamp(float(time))
    date = time.date()
    time = time.time()
    who = log[i].getElementsByTagName('nick')
    who = who[0].childNodes[0].nodeValue
    body = log[i].getElementsByTagName('body')
    body = body[0].childNodes[0].nodeValue
    if(opts.date != "all"):
        if year != date.year:
            continue
        if month != date.month:
            continue
        if day != date.day:
            continue
    if(opts.datebg != "all"):
        if yearbg > date.year:
            continue
        if yearbg == date.year and monthbg > date.month:
            continue
        if yearbg == date.year and monthbg == date.month and daybg > date.day:
            continue
    if(opts.dateend != "all"):
        if yearend < date.year:
            continue
        if yearend == date.year and monthend < date.month:
            continue
        if yearend == date.year and monthend == date.month and dayend < date.day:
            continue
    if(opts.timebg != "all"):
        if opts.timeforall:
            if int(hourbg) > int(time.hour):
                continue
            if int(hourbg) == int(time.hour) and int(minutebg) > int(time.minute):
                continue
        else:
            if yearbg > date.year:
                continue
            if yearbg == date.year and monthbg > date.month:
                continue
            if yearbg == date.year and monthbg == date.month and daybg > date.day:
                continue
            if yearbg == date.year and monthbg == date.month and daybg == date.day and int(hourbg) > int(time.hour):
                continue
            if yearbg == date.year and monthbg == date.month and daybg == date.day and int(hourbg) == int(time.hour) and int(minutebg) > int(time.minute):
                continue
    if(opts.timeend != "all"):
        if opts.timeforall:
            if int(hourend) < int(time.hour):
                continue
            if int(hourend) == int(time.hour) and int(minuteend) < int(time.minute):
                continue
        else:
            if yearend < date.year:
                continue
            if yearend == date.year and monthend < date.month:
                continue
            if yearend == date.year and monthend == date.month and dayend < date.day:
                continue
            if yearend == date.year and monthend == date.month and dayend == date.day and int(hourend) < int(time.hour):
                continue
            if yearend == date.year and monthend == date.month and dayend == date.day and int(hourend) == int(time.hour) and int(minuteend) < int(time.minute):
                continue
    if(opts.search or opts.search2):
        if not s.findall(body):
            continue
    if(date != pdate):
        print cmagenta + str(date)
        pdate = date
    print cblue + "    " + str(time) + cgreen + " " + who + cwhite + " " + body[1:]
