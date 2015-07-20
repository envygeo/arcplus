#@+leo-ver=5-thin
#@+node:maphew.20120201135209.1853: * @file AttributedMultiRingBuffer.py
''' multi-ring-buffer.py: Create multiple ring buffers, keeping named attributes of parent feature class.

Process:
    - create inside only buffer for each of the specifed buffer widths
    - store buffer width used as an attribute
    - merge all buffers into a single feature class, ensuring largest width first so narrower ones are drawn on top

Usage:
    multi-ring-buffer [feature class]  [workspace]  [output feature class]  [widths list]  [attributes to keep]
    
    multi-ring-buffer R:\data.gdb\Foobar_ply  X:\maps\buffers.gdb  Foobar_rings   50,-50,-100,-300,-600  NAME,TYPE
   
Workspace must exist.
The width and attribute parameters must be comma separated and have no spaces.

Requires Arcgis 10, Arcinfo license level.

(c) 2012 Environment Yukon, matt.wilkie@gov.yk.ca
Licensed under the MIT license: http://www.opensource.org/licenses/MIT

Also see http://gis.stackexchange.com/questions/19505/multiple-ring-buffer-with-attributes
'''

import arcpy
from arcpy import env

in_fc = arcpy.GetParameterAsText(0)                   # features to buffer
wspace = arcpy.GetParameterAsText(1)                # output workspace
out_fc = arcpy.GetParameterAsText(2)                 # finished result
distances = arcpy.GetParameterAsText(3).split(',')  # list of buffer widths 
# parse list of attributes to keep into semi-colon separated as expected by buffer tool
dissolveFields = arcpy.GetParameterAsText(4).replace(',',';')

env.workspace = wspace

sideType = "OUTSIDE_ONLY"
endType = "ROUND"
dissolveType = "LIST"
#dissolveFields = "NAME;TYPE"    # attributes we want to keep, adjust as needed 

buffered_fcs = []
for distance in distances:
    buf_fc = arcpy.ValidateTableName('xxx_' + out_fc + distance)
    print("...buffering {0} into {1} with width {2}".format(in_fc, buf_fc, distance))
    
    arcpy.Buffer_analysis(in_fc, buf_fc, distance, sideType, endType, dissolveType, dissolveFields)
    
    # store buffer width as attribute value
    arcpy.AddField_management(buf_fc, 'Width', "TEXT", "", "", 16)
    arcpy.CalculateField_management(buf_fc, 'Width', distance, "PYTHON")
    
    buffered_fcs.append(buf_fc)

# arrange buffers from largest to smallest width
# so the draw order is correct after merging
buffered_fcs.sort()
buffered_fcs.reverse() 

print("...Merging intermediate buffers into {0}".format(out_fc))
arcpy.Merge_management(buffered_fcs, out_fc)

# remove temporary intermediate files
print("...Removing intermediate files")
for fc in arcpy.ListFeatureClasses('xxx_*'):
    arcpy.Delete_management(fc)
#@-leo
