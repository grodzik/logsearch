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
import re
import ekg
import string
import os

cred = "\033[01;31m"
cgreen = "\033[01;32m"
cyellow = "\033[01;33m"
cblue = "\033[01;34m"
cmagenta = "\033[01;35m"
ccyan = "\033[01;36m"
cwhite = "\033[01;37m"

def search(name, args):
    args = args.split(" ")
    date = "all"
    datebg = "all"
    dateend = "all"
    timebg = "all"
    timeend = "all"
    timeforall = 0
    search = ""
    search2 = ""
    curtime = datetime.now()
    user = str(ekg.window_current())
    for x in range(len(args)-1):
        if args[x] == "-d":
            date = args[x+1]
            x += 1
        elif args[x] == "-db":
            datebg = args[x+1]
            x += 1
        elif args[x] == "-de":
            dateend = args[x+1]
            x += 1
        elif args[x] == "-tb":
            timebg = args[x+1]
            x += 1
        elif args[x] == "-te":
            timeend = args[x+1]
            x += 1
        elif args[x] == "-tfa":
            timeforall = 1
        elif args[x] == "-u":
            user = args[x+1]
            x += 1
        elif args[x] == "-s":
            search = string.join(args[x+1:], " ")
            x = len(args)
    sessions = ekg.sessions()
    user = str.lower(user)
    b = 0
    for x in sessions:
        for u in x.users():
            if str.lower(str(u.nickname)) == user or str.lower(str(u.uid)) == user:
                user = "/%s/%s.xml" % (str(x),u.uid)
                b = 1
                break
        if b == 1:
            break
    if b == 0:
        return 1
    if len(ekg.config['logsearch:logdir_path']):
        user = ekg.config['logsearch:logdir_path'] + user
    else:
        user = os.environ["HOME"] + "/.ekg2/logs/" + user
    if(date != "all"):
        r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
        if not (r.match(date)):
            ekg.echo("Bledny format daty. Format: YYYY-MM-DD")
            return 0
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        if(year > int(curtime.year)):
            ekg.echo("Bledny rok")
            return 0
        elif(month > int(curtime.month) and (month > 12 or month <= 0)):
            ekg.echo("Bledny miesiac")
            return 0
        elif(day > int(curtime.day) and (day > 31 or day <= 0)):
            ekg.echo("Bledny dzien")
            return 0
        datebg = "all"
        dateend = "all"
    else:
        if(datebg != "all"):
            r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
            if not (r.match(datebg)):
                ekg.echo("Bledny format daty. Format: YYYY-MM-DD")
                return 0
            yearbg = int(datebg[0:4])
            monthbg = int(datebg[5:7])
            daybg = int(datebg[8:10])
            if(yearbg > int(curtime.year)):
                ekg.echo("Bledny rok")
                return 0
            elif(monthbg > int(curtime.month) and (monthbg > 12 or monthbg <= 0)):
                ekg.echo("Bledny miesiac")
                return 0
            elif(daybg > int(curtime.day) and (daybg > 31 or daybg <= 0)):
                ekg.echo("Bledny dzien")
                return 0
        if(dateend != "all"):
            r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
            if not (r.match(dateend)):
                ekg.echo("Bledny format daty. Format: YYYY-MM-DD")
                return 0
            yearend = int(dateend[0:4])
            monthend = int(dateend[5:7])
            dayend = int(dateend[8:10])
            if(yearend > int(curtime.year)):
                ekg.echo("Bledny rok")
                return 0
            elif(monthend > int(curtime.month) and (monthend > 12 or monthend <= 0)):
                ekg.echo("Bledny miesiac")
                return 0
            elif(dayend > int(curtime.day) and (dayend > 31 or dayend <= 0)):
                ekg.echo("Bledny dzien")
                return 0

    if(timebg != "all"):
        r = re.compile("[0-9]{2}:[0-9]{2}")
        if not (r.match(timebg)):
            ekg.echo("Bledny format czasu poczatkowego. Format: HH:MM")
            return 0
        hourbg = int(timebg[0:2])
        minutebg = int(timebg[3:5])
        if(hourbg < 0 or hourbg >= 24):
            ekg.echo("Bledna godzina")
            return 0
        if(minutebg < 0 or minutebg >= 60):
            ekg.echo("Bledne minuty")
            return 0
        if(date == "all" and datebg == "all"):
            yearbg = int(curtime.year)
            monthbg = int(curtime.month)
            daybg = int(curtime.day)

    if(timeend != "all"):
        r = re.compile("[0-9]{2}:[0-9]{2}")
        if not (r.match(timeend)):
            ekg.echo("Bledny format czasu poczatkowego. Format: HH:MM")
            return 0
        hourend = int(timeend[0:2])
        minuteend = int(timeend[3:5])
        if(hourend < 0 or hourend >= 24):
            ekg.echo("Bledna godzina")
            return 0
        if(minuteend < 0 or minuteend >= 60):
            ekg.echo("Bledne minuty")
            return 0
        if(date == "all" and dateend == "all"):
            yearend = int(curtime.year)
            monthend = int(curtime.month)
            dayend = int(curtime.day)

    if search:
        s = re.compile(search, re.IGNORECASE)

    if search2:
        s = re.compile(search2)

    log = minidom.parse(user)
    log = log.getElementsByTagName('message')

    tmpdate = ""
    pdate = ""

    strtoprint = "\n"

    for i in range(0, log.length):
        time = log[i].getElementsByTagName('received')
        time = time[0].childNodes[0].nodeValue
        time = datetime.fromtimestamp(float(time))
        tmpdate = time.date()
        time = time.time()
        who = log[i].getElementsByTagName('nick')
        who = who[0].childNodes[0].nodeValue
        body = log[i].getElementsByTagName('body')
        body = body[0].childNodes[0].nodeValue
        if(date != "all"):
            if year != tmpdate.year:
                continue
            if month != tmpdate.month:
                continue
            if day != tmpdate.day:
                continue
        if(datebg != "all"):
            if yearbg > tmpdate.year:
                continue
            if yearbg == tmpdate.year and monthbg > tmpdate.month:
                continue
            if yearbg == tmpdate.year and monthbg == tmpdate.month and daybg > tmpdate.day:
                continue
        if(dateend != "all"):
            if yearend < tmpdate.year:
                continue
            if yearend == tmpdate.year and monthend < tmpdate.month:
                continue
            if yearend == tmpdate.year and monthend == tmpdate.month and dayend < tmpdate.day:
                continue
        if(timebg != "all"):
            if timeforall:
                if int(hourbg) > int(time.hour):
                    continue
                if int(hourbg) == int(time.hour) and int(minutebg) > int(time.minute):
                    continue
            else:
                if yearbg > tmpdate.year:
                    continue
                if yearbg == tmpdate.year and monthbg > tmpdate.month:
                    continue
                if yearbg == tmpdate.year and monthbg == tmpdate.month and daybg > tmpdate.day:
                    continue
                if yearbg == tmpdate.year and monthbg == tmpdate.month and daybg == tmpdate.day and int(hourbg) > int(time.hour):
                    continue
                if yearbg == tmpdate.year and monthbg == tmpdate.month and daybg == tmpdate.day and int(hourbg) == int(time.hour) and int(minutebg) > int(time.minute):
                    continue
        if(timeend != "all"):
            if timeforall:
                if int(hourend) < int(time.hour):
                    continue
                if int(hourend) == int(time.hour) and int(minuteend) < int(time.minute):
                    continue
            else:
                if yearend < tmpdate.year:
                    continue
                if yearend == tmpdate.year and monthend < tmpdate.month:
                    continue
                if yearend == tmpdate.year and monthend == tmpdate.month and dayend < tmpdate.day:
                    continue
                if yearend == tmpdate.year and monthend == tmpdate.month and dayend == tmpdate.day and int(hourend) < int(time.hour):
                    continue
                if yearend == tmpdate.year and monthend == tmpdate.month and dayend == tmpdate.day and int(hourend) == int(time.hour) and int(minuteend) < int(time.minute):
                    continue
        if(search or search2):
            if not s.findall(body):
                continue
        if(tmpdate != pdate):
            strtoprint += cmagenta + str(tmpdate) + "\n"
            pdate = tmpdate
        strtoprint += cblue + "    " + str(time) + cgreen + " " + who + cwhite + " " + body[1:] + "\n"
    ekg.echo(strtoprint)


ekg.command_bind('logsearch', search)
ekg.variable_add('logsearch:logdir_path', os.environ["HOME"] + "/.ekg2/logs/")
