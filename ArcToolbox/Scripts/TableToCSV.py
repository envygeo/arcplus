'''
Tool:    Table to CSV
Source:  TableToCSV.py
Author:  Matt.Wilkie@gov.yk.ca
License: X/MIT, (c) 2014 Environment Yukon

Export a table to comma delimited text file (CSV)

Required Arguments:
    {path to}\input table
    {path to}\output.csv


Courtesy of Jason on "Export table to X,Y,Z ASCII file via arcpy"
@url http://gis.stackexchange.com/a/17934/108
'''
import arcpy
import csv

def table2csv(table, outfile):
  #--first lets make a list of all of the fields in the table
  fields = arcpy.ListFields(table)
  field_names = [field.name for field in fields]

  with open(outfile,'wb') as f:
      dw = csv.DictWriter(f,field_names)
      #--write all field names to the output file
      dw.writeheader()

      #--now we make the search cursor that will iterate through the rows of the table
      with arcpy.da.SearchCursor(table,field_names) as cursor:
          for row in cursor:
              dw.writerow(dict(zip(field_names,row)))


if __name__ == "__main__":
    ''' Gather tool inputs and pass them to main function '''

    table = arcpy.GetParameterAsText(0)
    outfile = arcpy.GetParameterAsText(1)
    table2csv(table, outfile)
    
