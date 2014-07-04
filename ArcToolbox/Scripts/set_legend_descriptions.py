'''
Set description property of Unique Value legend items from a lookup table. Enables having a legend with lengthy descriptions as well as the record values.

Example:

[SB]      Black Spruce	Black spruce diagnostic and dominant in sparse tree and 
          shrub overstory; shrub birch, willow and low ericaceous shrubs also common. 
          Extensive moss groundcover, Sphagnum present. Established on permafrost and 
          poorly drained sites at lower elevations.
      
[D/G/Li]  Mat vegetation dominated by Dryas and diverse lichens; graminoids 
          significant but sparse. Ericaceous groundshrubs and prostate willows 
          common. Typical on exposed sites at higher elevations.


Adapted from 
http://gis.stackexchange.com/questions/102956/setting-symbol-descript_table-of-arcmap-layout-legends-from-table
'''
import arcpy

# name and path of the lookup table
lookup_table = r"T:\ENV.344\SDR\ENV344.gdb\vegMajorComm_Lookup"

# change these to match the relevant field names in the lookup table
code = 'VegCode'
description = 'Description'

map_name = r"..\map\test_map.mxd"           
layer_name = "Vegetation Communities"
output_map = r"..\map\test_map_descrip.mxd"

## --- shouldn't need to change anything below here ---

# build the descriptions dictionary
descriptions = {}
rows = arcpy.SearchCursor(lookup_table)
for item in rows:
    #print item.getValue(code), item.getValue(description)
    descriptions[item.getValue(code)] = item.getValue(description)

mxd = arcpy.mapping.MapDocument(map_name)
lyr = arcpy.mapping.ListLayers(mxd, layer_name)[0]

# lyr.symbology requires the classValues and classDescriptions to have
# same number of rows and be in same order. So extract only matching 
# elements from the description dictionary
desclist = []
if lyr.symbologyType == "UNIQUE_VALUES":

    #extract matches
    for symbol in lyr.symbology.classValues:
      desclist.append(descriptions[symbol])    
    
    # assign the descriptions
    lyr.symbology.classDescriptions = desclist


mxd.saveACopy(output_map)
del mxd