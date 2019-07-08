''' Generate list of possible geoprocessing error codes. These error codes are
   not documented in the help anymore so Curtis wrote a script to make a list.
   Initial version: 2019-Jul-05, Curtis Price <cprice@usgs.gov>
'''
import sys
import arcpy

# start code to fetch
try:
  n = int(sys.argv[1])
except IndexError:
  print('''Usage: gpcodes [start number] {optional end number}\n''')
  sys.exit()

# optional end code to fetch
try:
  nn = int(sys.argv[2])
except IndexError:
  nn = n # default to start number

nn += 1 # increment by 1 so we return the final code as well

for k in range(n,nn):
  try:
    dsc = arcpy.GetIDMessage(k)
    if dsc:
        print("{:6d}\t{}".format(k, dsc))
  except:
    pass
