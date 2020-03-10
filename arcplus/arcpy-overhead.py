from timeit import default_timer as timer
start = timer()
from datetime import datetime, timedelta

from uuid import uuid4
eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

start_arc = timer()
import arcpy
done_arc = timer() - start_arc

import os
machine = os.environ['COMPUTERNAME']

d = arcpy.GetInstallInfo()
print("{:12} {:10} {:10} {:10} {:10} {:>10} {:>56}".format("Machine",
    "Product",
    "Version",
    "Build",
    "License",
    "LoadArcpy",
    "EventID"))

print("{:12} {:10} {:10} {:10} {:10} {:>10} {:>56}".format(machine,
    d['ProductName'],
    d['Version'],
    d['BuildNumber'],
    d['LicenseLevel'],
    round(done_arc,3),
    eventid))
