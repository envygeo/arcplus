'''
Tool Name:   Create layer from selected features
Version:     ArcGIS 10.3
Author:      Matt.Wilkie@gov.yk.ca
Started:     2015-Apr-07
License:     X/MIT, (c) 2015 Environment Yukon

Required Arguments:
         Layer with selected features

Description:
        Create in-memory layer using only selected features of the input layer. Basically this is to replicate the functionality of "{Layer} >> r-click >> Selection >> Create Layer from Selected Features" in a manner that can used in a python script.

Adapted from @Pete		
http://gis.stackexchange.com/questions/63717/use-a-selection-of-features-in-arcmap-in-python-script/63743#63743
'''
import arcpy
from arcpy import env

def main(layer):
	arcpy.env.workspace = "in_memory"

	layer = "The Feature Class with the selection"
	results_layer = layer + "_selection"

	#this will create a new feature class from the selected features but will do it In Memory
	arcpy.CopyFeatures_management(layer, results_layer)

	#Now do all the other stuff you want like convert it to a layer and work with it
	arcpy.MakeFeatureLayer_management(results_layer)
    

if __name__ == "__main__":
    ''' Gather tool inputs and pass them to gpxToPoints(file, outputFC) '''
    layer = arcpy.GetParameterAsText(0)
    main(layer)
