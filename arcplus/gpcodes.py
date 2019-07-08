''' Generate list of possible geoprocessing error codes. These error codes are
   not documented in the help anymore so Curtis wrote a script to make a list.
   Curtis Price <cprice@usgs.gov>, 2019-Jul-05
'''
import sys
import arcpy
try:
  n = int(sys.argv[1])
except:
  n = 20
for k in range(n):
  try:
    dsc = arcpy.GetIDMessage(k)
    if dsc:
        print("{:6d} {}".format(k, dsc))
  except:
    pass
