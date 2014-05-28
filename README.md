arcplus
=======
*a few little things I think Esri's arcpy and related should have*


## arcplus.py
A python module for easy re-use; has only one function at the moment. 

#### listAllFeatureClasses
Recursively list all Feature Classes in a geodatabase or coverage (normal listFeatureClasses method does not recurse)

See [Listing all feature classes in File Geodatabase, including within feature datasets?](http://gis.stackexchange.com/questions/5893/listing-all-feature-classes-in-file-geodatabase-including-within-feature-datase)

## Scripts

#### GPXtoFeaturesXY.py

A small enchancement to Esri's GPXtoFeatures.py: store the original geographic coordinates as attributes.

####  metadata_batch_upgrade.py

Recursively walk through a GDB or workspace and upgrades the metadata record of any feature class found.

Regular upgrade tool can only do one FC at a time, and using the batch control is painful as you drill down into each dataset individually to drag and drop. 

#### TableToCSV.py

ArcGIS doesn't have an out of the box tool for exporting a table to text. Let's fix that
[not working yet]

Inspiration: [Export table to X,Y,Z ASCII file via arcpy](http://gis.stackexchange.com/questions/17933/export-table-to-x-y-z-ascii-file-via-arcpy)



SysAdmin
--------

#### [uninstall-ALL-ArcGIS-products.bat](SysAdmin/uninstall-ALL-ArcGIS-products.md)

Uninstall ArcGIS products using the Windows Installer `msiexec`, feeding it a text file with Product IDs. Will not work for programs like ArcPad which don't use msi to install in the first place.  