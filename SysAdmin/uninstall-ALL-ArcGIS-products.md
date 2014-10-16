# uninstall-ALL-ArcGIS-products.bat

Uninstall ArcGIS products using the Windows Installer `msiexec`, feeding it a text file with Product IDs.

Will not work for programs like ArcPad which don't use msi to install in the first place.  

## Install
1. Download [uninstall-ALL-ArcGIS-products.bat](https://github.com/maphew/arcplus/blob/master/SysAdmin/uninstall-ALL-ArcGIS-products.bat) and save somewhere handy. 
2. Ditto for save the [product list](https://github.com/maphew/arcplus/blob/master/SysAdmin/product-codes.txt) *(last updated 2014-Oct-16)*, or make your own.


## Usage  
    uninstall-ALL-ArcGIS-products product-codes.txt
    uninstall-ALL-ArcGIS-products product-codes.txt /silent

---------
Product codes were taken from [Esri KB 28709 - Silently uninstall ArcGIS products](http://support.esri.com/en/knowledgebase/techarticles/detail/28709) *(Last Modified: 11/2/2012)*

The list in that page is not complete. Product Codes for most Esri setups can be found in the setup.ini file delivered with the other installation files. (Please feel free to issue a pull request if you find product codes we're missing here. Also please feel free to contribute an .ini scraper!)

### Syntax of *product-codes.txt*

    Product Name {a1a1a1a-a1a1a-a1a1a...}
    
    ArcGIS 8.2
    ArcGIS Desktop {A149DEA2-1D5B-11D5-9F76-00C04F6BC7A1}
    ArcGIS ArcObjects Developer Kit {52069752-B5E9-11D5-8110-00C04FA070E5}
    ArcGIS Tutorial Data {440A069B-9016-11D4-80CB-00C04FA070E5}
    ...etc.
    

-----
### Notes

An alternate approach for uninstalling, not used here, is to retrieve the product list dynamically from the local machine with [`wmic`](http://technet.microsoft.com/en-us/library/bb742610.aspx) (be patient, takes a very long time, appearing frozen, but isn't).

	wmic product where "Name like '%ArcGIS%'" ^
	get Name, IdentifyingNumber, Version 


Also see [The simplest way to uninstall any and all ArcGIS products?](http://gis.stackexchange.com/questions/49290/the-simplest-way-to-uninstall-any-and-all-arcgis-products)