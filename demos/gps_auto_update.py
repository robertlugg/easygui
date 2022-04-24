"""

from:
http://stackoverflow.com/questions/24621288/getting-easygui-to-self-update-info

Use this to show how the new interface would be used

"""

import sys
if sys.version_info.major > 2:
    print("Sorry, the module gps is not included in Python 3") 
    sys.exit()

import gps
from easygui import *
# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
while True:
     try:
          report = session.next()
          if report['class'] == 'TPV':
               if hasattr(report, 'time'):
                    hour = int(report.time[11:13])
                    hourfix = hour - 7
                    if hourfix < 12:
                         time = 'Current Time Is: ' + report.time[5:7] + '/' + report.time[8:10] + '/' + report.time[0:4] + ' ' + str(hourfix) + report.time[13:19] + ' am'
                    else:
                         hourfix = hourfix - 12
                         time =  'Current Time Is: ' + report.time[5:7] + '/' + report.time[8:10] + '/' + report.time[0:4] + ' ' + str(hourfix) + report.time[13:19] + ' pm'
          if report['class'] == 'TPV':
               if hasattr(report, 'speed'):
                    speed = int(report.speed * gps.MPS_TO_MPH)
                    strspeed = str(speed)
                    currentspeed = 'Current Speed Is: ' + strspeed + ' MPH'
                    msgbox(time + "\n" + currentspeed, "SPEEDO by Jono")
     except KeyError:
          pass
     except KeyboardInterrupt:
          quit()
     except StopIteration:
          session = None
          print("GPSD has terminated")