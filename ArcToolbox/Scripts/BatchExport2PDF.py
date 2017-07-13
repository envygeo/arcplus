## From http://www.arcgis.com/home/item.html?id=4ddd1323ae0d4ebe8f8250992faab0f4
##  Export MXD to PDF (Python Script & Toolbox Tool) 
##   by @bteranUFA

# modified by ESRI for use as a toolbox script tool
## imported sys to get the raw inputs and os to use for path separator
import arcpy, sys, os
# Set OverWrite if files already exist
arcpy.OverWriteOutput = 1

print "Enter folder path:"
#mapDoc = raw_input()
mapDoc = sys.argv[1]
print os.path.dirname(mapDoc)
# set a variable to the full path and file name of the MXD
fullnam = os.path.basename(mapDoc)
# Strip off the MXD file extension and store as string variable for use in the 'out_pdf'
nam = fullnam.strip(".mxd")
print nam

# Commented this out, since it doesnt need to be a parameter when you use the MXD name as the PDF name
##print "Enter save as name:"
##mapName = sys.argv[2]

map = arcpy.mapping
mxd = map.MapDocument(mapDoc)

map_document = mxd
#out_pdf = r"K:\projects" + "\\" + mapName + ".pdf"
#out_pdf = r"K:\projects" + os.sep + mapName + ".pdf"
#out_pdf = os.path.dirname(mapDoc) + os.sep + mapName + ".pdf"
out_pdf = os.path.dirname(mapDoc) + os.sep + nam + ".pdf"

# Set all the parameters as variables here:
data_frame = 'PAGE_LAYOUT'
resolution = "300"
image_quality = "NORMAL"
colorspace = "RGB"
compress_vectors = "True"
image_compression = "DEFLATE"
picture_symbol = 'RASTERIZE_BITMAP'
convert_markers = "False"
embed_fonts = "True"
layers_attributes = "NONE"
georef_info = "False"

# Due to a known issue, the df_export_width and df_export_height must be set to integers in the code:
map.ExportToPDF(map_document, out_pdf, data_frame, 640, 480, resolution, image_quality, colorspace, compress_vectors, image_compression, picture_symbol, convert_markers, embed_fonts, layers_attributes, georef_info)

# This gives feedback in the script tool dialog:
arcpy.GetMessages()