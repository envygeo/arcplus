'''Clip all layers in the map to the specified polygon.
Adapted from Alex Tereshenkov, http://gis.stackexchange.com/a/111712/108
'''
import os
import arcpy
arcpy.env.overwriteOutput = True

mxd = arcpy.GetParameterAsText(0)
clip_layer = arcpy.GetParameterAsText(1)
out_gdb = arcpy.GetParameterAsText(2)

if not mxd:
    mxd = arcpy.mapping.MapDocument("CURRENT")
else:
    mxd = arcpy.mapping.MapDocument(mxd)

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isBroken:
        arcpy.AddMessage('"%s"\t skipping broken layer' % lyr)
        continue
    elif not lyr.isGroupLayer:
        arcpy.AddMessage('"%s"\t Clipping...' % lyr)
        out_layer = os.path.join(out_gdb, lyr.name)
        if lyr.isFeatureLayer:
            arcpy.Clip_analysis(lyr, clip_layer, out_layer)
        elif lyr.isRasterLayer:
            arcpy.Clip_management(lyr, '#', out_layer, clip_layer, '#', 'ClippingGeometry')
        else:
            arcpy.AddMessage('"%s" skipping, not a Feature or Raster layer')
    else:
        if not lyr.isGroupLayer:
            arcpy.AddMessage('"%s"\t unknown layer type, dont know what to do with it.' % lyr)
            
            
print arcpy.GetMessages()
