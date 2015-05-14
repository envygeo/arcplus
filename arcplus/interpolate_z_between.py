'''
Interpolate missing Z values along a 3D line.

*** BROKEN ***

Adapted from @Tomek's work at
http://gis.stackexchange.com/a/18655/108
'''
from arcplus import ao

sPath = r'd:\s\test.gdb'
fcName = 'centerline'

# import arcobjects libraries
ao.GetStandaloneModules()
ao.InitStandalone()
import comtypes.gen.esriSystem as esriSystem
import comtypes.gen.esriGeoDatabase as esriGeoDatabase
import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

### Open the FGDB
##pWS = ao.Standalone_OpenFileGDB(gdb)

# open geodatabase and featureclass
pWSF = ao.NewObj(esriDataSourcesGDB.FileGDBWorkspaceFactory, esriGeoDatabase.IWorkspaceFactory)
pWS = pWSF.OpenFromFile(sPath, 0)
pFWS = pWS.QueryInterface(esriGeoDatabase.IFeatureWorkspace)
pFClass = pFWS.OpenFeatureClass(str(fcName))

# set update cursor on the featureclass
pFCursor = pFClass.Update(None, True)
pFeat = pFCursor.NextFeature()

# loop trough features in featureclass
while pFeat:
    print "--- Feature:", pFeat.OID
    pShape = pFeat.ShapeCopy # clone shape of current feature
    pIZ = pShape.QueryInterface(esriGeometry.IZ2) #set IZ interface on the data - allow for interpolation of the Z value
    IPointCollection = pShape.QueryInterface(esriGeometry.IPointCollection) # set IPointCollection interface on the data - allow for points manipulation within the point collection
    IPoint = ao.NewObj(esriGeometry.Point, esriGeometry.IPoint) # create Point object with IPoint interface
    pStart = 0 # set pStart parameter to index[0]

# loop trough IPointCollection within the polyline, find pStart and pEnd point within the polyline for IZ.InterpolateZsBetween
    for i in range(IPointCollection.PointCount):
        Point = IPointCollection.QueryPoint(i, IPoint) # query for point within the IPointCollection at index i and insert it in to IPoint

# selection of the pStart and pEnd properties based on points Z value and interpolation of the vertexes within the polyline
        if i==0: # skip value at index[0]
##            pass
            print '\tSkipping point:', i
            continue
        elif IPoint.Z != 0: # assign pEnd and pStart if Z value of the point (vertex) is larger than 0.01 (0.01 not 0 as 0 in arcgis is returned in python as 4.54747350886e-013)
            pEnd = i
            pIZ.InterpolateZsBetween(0,pStart,0,pEnd) # program assumes that is dealing with single part polylines
            pFeat.Shape = pIZ
            pFCursor.UpdateFeature(pFeat)
            pStart = pEnd
    pFeat = pFCursor.NextFeature()
