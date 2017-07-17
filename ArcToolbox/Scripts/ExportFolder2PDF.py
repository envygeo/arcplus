#Export a folder of maps to PDFs at their Map Document set sizes
#Written using ArcGIS 10 and Python 2.6.5
#by: Guest
# https://gis.stackexchange.com/questions/7147/how-to-batch-export-mxd-to-pdf-files

import arcpy, os, glob

#Read input parameter from user.
in_path = arcpy.GetParameterAsText(0)

# Set all the parameters as variables here:
data_frame = 'PAGE_LAYOUT'
df_export_width = 1920
df_export_height = 1200
resolution = "300"
image_quality = "BETTER"
colorspace = "RGB"
compress_vectors = "True"
image_compression = "ADAPTIVE"
picture_symbol = 'VECTORIZE_BITMAP'
convert_markers = "False"
embed_fonts = "True"
layers_attributes = "LAYERS_ONLY"
georef_info = "False"
jpeg_compression_quality = 85

exportPath =arcpy.GetParameterAsText(1)

maps = glob.glob(os.path.join(in_path, '*.mxd'))

for m in maps:
    dir, fname = os.path.split(m)                        # 'X:\path\to', 'some_map.mxd'
    basename = os.path.splitext(fname)[0]                # 'some_map'
    newPDF = os.path.join(exportPath, basename + '.pdf') # 'Y:\output\some_map.pdf'

    arcpy.AddMessage('Reading: ' + m)
    mxd = arcpy.mapping.MapDocument(m)
    arcpy.AddMessage('Writing: ' + newPDF)
    arcpy.mapping.ExportToPDF(mxd, newPDF, data_frame, df_export_width, df_export_height, resolution, image_quality,
                              colorspace, compress_vectors, image_compression, picture_symbol, convert_markers, embed_fonts,
                              layers_attributes, georef_info, jpeg_compression_quality)
    del mxd

arcpy.GetMessages()