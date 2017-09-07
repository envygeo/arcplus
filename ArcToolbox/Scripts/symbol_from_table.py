''' Set legend symbology from a raster attribute table

 Sources:
    - http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/uniquevaluessymbology-class.htm
 '''
import arcpy
mxd = arcpy.mapping.MapDocument("current")
lyr = arcpy.mapping.ListLayers(mxd, "Population")[0]
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"POP2000\" > 20000000")
stateList = []
rows = arcpy.da.SearchCursor(lyr, ["STATE_NAME"])
for row in rows:
  stateList.append(row[0])

if lyr.symbologyType == "UNIQUE_VALUES":
  lyr.symbology.classValues = stateList
  lyr.symbology.showOtherValues = False

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
del mxd