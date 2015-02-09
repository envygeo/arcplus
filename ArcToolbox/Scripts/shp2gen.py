#!/usr/bin/env python
#
# shp2gen.py
# Convert shapefile to arcinfo generate format
#
# Author: Matthew Perry
#
from osgeo import ogr, sys

if __name__ == "__main__":
    try:
        inputFile = sys.argv[1];
    except:
        print " usage: shp2gen.py input.shp > output.gen"
        sys.exit(1)

    # Open dataset and get layer
    ds = ogr.Open(inputFile)
    layer = ds.GetLayer()

    coords = ''
    feature = layer.GetNextFeature()
    fn = 0
    while feature is not None:
        coords = '';
        geom = feature.GetGeometryRef()
        geomtype = geom.GetGeometryType()
        if geomtype == ogr.wkbPoint:
            coords = coords + str(fn) + "," + str(geom.GetX(0)) + "," + \
                     str(geom.GetY(0)) + "\n";
        elif geomtype == ogr.wkbLineString or geomtype == ogr.wkbPolygon:
            geom = geom.GetGeometryRef(0)
            numpoints = geom.GetPointCount()
            coords = coords + str(fn) + "\n"
            for i in range(numpoints):
                coords = coords + str(geom.GetX(i)) + " " + \
                         str(geom.GetY(i)) + "\n";
            coords = coords + "END"

        feature.Destroy()
        feature = layer.GetNextFeature()
        fn = fn+1
        if coords != '':
            print coords

    print 'END'
    ds.Destroy()
