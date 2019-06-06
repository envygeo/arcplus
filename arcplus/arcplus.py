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

def listAllFeatureClasses (gdb,**kwargs):
    import arcpy
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

def layer_from_selected(layer):
    ''' Create in-memory layer using only selected features of the input layer.

        Basically this is to replicate the functionality of "{Layer} >> r-click >> Selection >> Create Layer from Selected Features" in a manner that can used in a python script.

        Arguments:  Layer with selected features

    Adapted from @Pete
    http://gis.stackexchange.com/questions/63717/use-a-selection-of-features-in-arcmap-in-python-script/63743#63743
    '''
    import arcpy
    arcpy.env.workspace = "in_memory"
    results_layer = layer + "_selection"
    #this will create a new feature class from the selected features but will do it In Memory
    arcpy.CopyFeatures_management(layer, results_layer)
    #Now do all the other stuff you want like convert it to a layer and work with it
    arcpy.MakeFeatureLayer_management(results_layer)
    return


