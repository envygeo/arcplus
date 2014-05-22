'''
Tool Name:   Metadata Batch Upgrade
Source Name: metadata_batch_upgrade.py
Version:     ArcGIS 10.2.2
Author:      Matt.Wilkie@gov.yk.ca
Started:     2013-May-16
License:     X/MIT, (c) 2014 Environment Yukon

Required Arguments:
         Input Geodatabase or Workspace: path to gdb or workspace

Description:
        Recursively walk through a GDB or workspace and upgrades the metadata record of any feature class found.

'''

import arcpy
import arcplus

def main(gdb):
    fcs = arcplus.listAllFeatureClasses(gdb)
    for fc in fcs:
        print "magic happens with: ", fc
        arcpy.UpgradeMetadata_conversion(
            Source_Metadata=fc,
            Upgrade_Type="FGDC_TO_ARCGIS")
        print arcpy.GetMessages()
    

if __name__ == "__main__":
    ''' Gather tool inputs and pass them to gpxToPoints(file, outputFC) '''

    gdb = arcpy.GetParameterAsText(0)
    main(gdb)
