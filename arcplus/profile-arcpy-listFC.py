import arcpy

gdb = r'X:\Env-dat.081\source\yt_courbe_niveau_imperial.gdb'


def arcpy_listFC(gdb):
    arcpy.env.workspace = gdb
    print 'Looking in "%s" ' % (arcpy.env.workspace)
    fcs = arcpy.ListFeatureClasses()
    return fcs

arcpy_listFC(gdb)
