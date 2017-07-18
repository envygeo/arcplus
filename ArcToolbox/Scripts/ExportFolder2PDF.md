## Export Folder 2 PDF

Export all `mxd` within Input Folder to PDF.

### Install

Download `ArcPlus.tbx` and `Scripts\ExportFolder2PDF.py` and save somewhere useful (e.g. `D:\Arcplus`)


### Toolbox Usage

Same as all other tools, navigate to D:\Arcplus\Arcplus.tbx and double-click *Export Folder to PDF*.

Input Folder is required.
Output Folder is optional (if blank Input Folder is used).


### Command Line Usage

    python d:\Arcplus\Scripts\ExportFolder2PDF.py ^
      T:\Project042\Maps ^
      E:\Exports

## Notes ##

For now all [PDF options][0] are hard coded (pull requests to turn then into parameters welcome).

    data_frame = 'PAGE_LAYOUT'
    df_export_width = 1920  # ignored when using PAGE_LAYOUT
    df_export_height = 1200
    resolution = '300'
    image_quality = 'BEST'
    colorspace = 'RGB'
    compress_vectors = 'True'
    image_compression = 'ADAPTIVE'
    picture_symbol = 'VECTORIZE_BITMAP'
    convert_markers = 'False'
    embed_fonts = 'True'
    layers_attributes = 'LAYERS_ONLY'
    georef_info = 'True'
    jpeg_compression_quality = 85


 [0]: http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/exporttopdf.htm