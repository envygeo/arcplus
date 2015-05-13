arcplus
=======
*a few little things I think Esri's arcpy and related should have*


## Quick Start

 1. Open a [pip](https://pip.pypa.io/en/latest/installing.html) and an ArcGIS python enabled command shell, then install *[patched comtypes](https://github.com/enthought/comtypes/pull/75)* and *arcplus*:
	
	    pip install https://github.com/maphew/comtypes/archive/patch-1.zip
	    pip install https://github.com/maphew/arcplus/archive/master.zip

 2. Run python and:

    ``` 
    d:\>python
    Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import arcplus   
    
    >>> for fc in arcplus.listAllFeatureClasses(r"D:\scratch.gdb"):
    ...     print fc
    ...
    Looking in D:\scratch.gdb for "*"
    Administration_Boundaries\LI_1210009_2
    Administration_Boundaries\Yukon_Ditch_ENV080
    base_toponomy\Highway_shields
    base_toponomy\Physiographic_text
    base_toponomy\Places_text
    annotation_attrib_test
    fraser_peak_GPXtoFeatures
    ...
    ```     



#### arcplus.listAllFeatureClasses
Recursively list all Feature Classes in a geodatabase or coverage (normal listFeatureClasses method does not recurse)

See [Listing all feature classes in File Geodatabase, including within feature datasets?](http://gis.stackexchange.com/questions/5893/listing-all-feature-classes-in-file-geodatabase-including-within-feature-datase)

#### arcplus.ao
See [Use Arcobjects from Python](http://gis.stackexchange.com/questions/80/how-do-i-access-arcobjects-from-python/)

*...not working reliably yet!*

    >>> from arcplus import ao
    
    >>> ao.GetLibPath()
    u'C:\\ArcGIS\\Desktop10.3\\com\\'

    >>> dir(ao)
    ['ArcCatalog_GetSelectedTable',
     'ArcMap_AddTextElement',
     'ArcMap_GetEditWorkspace',
     'ArcMap_GetSelectedGeometry',
     'ArcMap_GetSelectedTable',
     'CLSID',
     'CType',
     'GetApp',
     'GetCurrentApp',
     'GetDesktopModules',
     'GetLibPath',
     'GetModule',
     'GetStandaloneModules',
     'InitStandalone',
     'Msg',
     'NewObj',
     'Standalone_CreateTable',
     'Standalone_OpenFileGDB',
     'Standalone_OpenSDE',
     'Standalone_QueryDBValues',
     '__builtins__',
     '__doc__',
     '__file__',
     '__name__',
     '__package__',
     '__path__',
     'ao']




## Scripts

#### clip_all_layers.py

Clip all layers in map to the specified polygon layer. Command line usage:

    clip_all_layers "path\to\Some map.mxd" path\to\data.gdb\clip_poly path\to\destination.gdb

Relative paths are interpreted relative to the mxd, not the current shell folder ([ref](http://gis.stackexchange.com/a/136826/108)).
There's an example toolbox usage in the Tests folder.

Built to support [building a map package with clippping](http://gis.stackexchange.com/questions/132352/arcgis-desktop-map-package-with-clipping).


#### GPXtoFeaturesXY.py

A small enchancement to Esri's GPXtoFeatures.py: store the original geographic coordinates as attributes.

####  metadata_batch_upgrade.py

Recursively walk through a GDB or workspace and upgrades the metadata record of any feature class found.

Regular upgrade tool can only do one FC at a time, and using the batch control is painful as you drill down into each dataset individually to drag and drop.

#### set_legend_descriptions.py
 
Set description property of Unique Value legend items from a lookup table. Enables having a legend with lengthy descriptions as well as the record values.

Adapted from [Setting symbol descriptions of ArcMap layout legends from table?](http://gis.stackexchange.com/questions/102956/setting-symbol-descriptions-of-arcmap-layout-legends-from-table/)


#### TableToCSV.py

ArcGIS doesn't have an out of the box tool for exporting a table to text. Let's fix that
[not working yet]

Inspiration: [Export table to X,Y,Z ASCII file via arcpy](http://gis.stackexchange.com/questions/17933/export-table-to-x-y-z-ascii-file-via-arcpy)



SysAdmin
--------

#### [uninstall-ALL-ArcGIS-products.bat](SysAdmin/uninstall-ALL-ArcGIS-products.md)

Uninstall ArcGIS products using the Windows Installer `msiexec`, feeding it a text file with Product IDs. Will not work for programs like ArcPad which don't use msi to install in the first place.  