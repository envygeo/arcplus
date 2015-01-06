'''
Tool:    Change Datasource Paths
Source:  change_datasource_paths.py
Author:  Matt.Wilkie@gov.yk.ca
License: X/MIT, (c) 2011 Environment Yukon

When data has moved to a different workspace AND feature dataset the regular
`findAndReplaceWorkspacePath` does not work. This script rectifies that.


Required Arguments:
    - layer file to re-path
    - new path to workspace containing the feature class
    - where to save the layer files

More information:
http://gis.stackexchange.com/questions/6884/change-data-source-path-in-lyr-files-in-arcgis-10
'''
import arcpy, os

# layer file to re-path
fname = arcpy.GetParameterAsText(0)
# new path to workspace containing the feature class
target_wspace = arcpy.GetParameterAsText(1)
# where to save the layer files
savedir = arcpy.GetParameterAsText(2)

lyr = arcpy.mapping.Layer(fname)

fixed_fname = os.path.join(savedir, lyr.longName)

print '\nOld layer properties (%s)' % (fname)
print 'workspace:\t', lyr.workspacePath
print 'full path:\t', lyr.dataSource

try:
    lyr.replaceDataSource(target_wspace, 'FILEGDB_WORKSPACE', lyr.datasetName, True)
    lyr.saveACopy(fixed_fname)
except:
    print arcpy.GetMessages()

print '\nNew layer properties (%s)' % (fixed_fname)
print 'workspace:\t', lyr.workspacePath
print 'full path:\t', lyr.dataSource

del lyr
