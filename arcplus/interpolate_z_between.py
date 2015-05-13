'''
Interpolate missing Z values along a 3D line.

Adapted from @Tomek's work at
http://gis.stackexchange.com/a/18655/108
'''

# import arcobjects liberaries
esriSystem = GetModule("C:/Program Files (x86)/ArcGIS/Desktop10.0/com/esriSystem.olb")
esriGeometry = GetModule("C:/Program Files (x86)/ArcGIS/Desktop10.0/com/esriGeometry.olb")
esriDataSourcesGDB = GetModule("C:/Program Files (x86)/ArcGIS/Desktop10.0/com/esriDataSourcesGDB.olb")
esriGeoDatabase = GetModule("C:/Program Files (x86)/ArcGIS/Desktop10.0/com/esriGeoDatabase.olb")

# open geodatabase and featureclass
pWSF = CreateObject(esriDataSourcesGDB.FileGDBWorkspaceFactory, interface=esriGeoDatabase.IWorkspaceFactory)
pWS = pWSF.OpenFromFile(str(DbPath), 0)
pFWS = pWS.QueryInterface(esriGeoDatabase.IFeatureWorkspace)
pFClass = pFWS.OpenFeatureClass(str(fcName))

# set update cursor on the featureclass
pFCursor = pFClass.Update(None, True)
pFeat = pFCursor.NextFeature()

# loop trough features in featureclass
while pFeat:
    pShape = pFeat.ShapeCopy # clone shape of current feature
    pIZ = pShape.QueryInterface(esriGeometry.IZ2) #set IZ interface on the data - allow for interpolation of the Z value
    IPointCollection = pShape.QueryInterface(esriGeometry.IPointCollection) # set IPointCollection interface on the data - allow for points manipulation within the point collection
    IPoint = CreateObject(esriGeometry.Point, interface=esriGeometry.IPoint) # create Point object with IPoint interface
    pStart = 0 # set pStart parameter to index[0]

# loop trough IPointCollection within the polyline, find pStart and pEnd point within the polyline for IZ.InterpolateZsBetween
    for i in range(IPointCollection.PointCount):
        Point = IPointCollection.QueryPoint(i, IPoint) # query for point within the IPointCollection at index i and insert it in to IPoint

# selection of the pStart and pEnd properties based on points Z value and interpolation of the vertexes within the polyline
        if i==0: # skip value at index[0]
            pass
        elif IPoint.Z != 0: # assign pEnd and pStart if Z value of the point (vertex) is larger than 0.01 (0.01 not 0 as 0 in arcgis is returned in python as 4.54747350886e-013)
            pEnd = i
            pIZ.InterpolateZsBetween(0,pStart,0,pEnd) # program assumes that is dealing with single part polylines
            pFeat.Shape = pIZ
            pFCursor.UpdateFeature(pFeat)
            pStart = pEnd
    pFeat = pFCursor.NextFeature()

def main():
    pass

if __name__ == '__main__':
    main()
