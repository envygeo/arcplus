''' 
Module:  arcplus
Source:  arcplus.py
Author:  Matt.Wilkie@gov.yk.ca
License: X/MIT, (c) 2014 Environment Yukon

Functions missing from regular ol' arcpy module


Place with your other code or PYTHONPATH and then:

    import arcplus
    fcs = arcplus.cool_extra_function(...)
    for fc in fcs:
        print "magic happens with: ", fc

(there is only one extra function at the moment... ;-) 
'''

import os
import arcpy

def listAllFeatureClasses (gdb,**kwargs):
    ''' 
    list all Feature Classes in a geodatabase or coverage recursively
    (normal listFeatureClasses does not recurse)

        import arcplus
        fcs = arcplus.listAllFeatureClasses('d:\default.gdb')
        for fc in fcs:
            print "magic happens with: ", fc

    Arcplus also adds wildcard filtering; to process only feature classes 
    that start with "HD_" within feature datasets containing "Hydro"

        fcs = arcplus.listAllFeatureClasses(gdb, fd_filter='*Hydro*', fc_filter='HD_*')
    '''

    arcpy.env.workspace = gdb

    if not kwargs.has_key('fc_filter'): fc_filter = '*'
    else: fc_filter = kwargs ['fc_filter']

    if not kwargs.has_key('fd_filter'): fd_filter = '*'
    else: fd_filter = kwargs ['fd_filter']

    print 'Looking in %s for "%s" ' % (arcpy.env.workspace,fc_filter)

    fcs = []
    for fds in arcpy.ListDatasets(fd_filter,'feature') + ['']:
        for fc in arcpy.ListFeatureClasses(fc_filter,'',fds):
            #print '%s\\%s' % (fds,fc)
            fcs.append(os.path.join(fds,fc))

    return fcs
