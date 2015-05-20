import arcpy

gdb = r'd:\s\test.gdb'
fc_stream = 'test_vtx_wtc'
fc_contour = 'test_vtx_ctr'
fc_result = 'test_result'

arcpy.env.workspace = gdb
geometries = arcpy.CopyFeatures_management(fc_stream, arcpy.Geometry())


def read_stream(fc_stream, fc_contour):
    g_ctr = arcpy.CopyFeatures_management(fc_contour, arcpy.Geometry())
    g = g_ctr[0]

    for row in arcpy.da.SearchCursor(fc_stream, ["OID@", "SHAPE@"]):
        print("Feature {0}:".format(row[0]))
        partnum = 0
        for part in row[1]:
            print("Part {0}:".format(partnum))

            # Step through each vertex in the feature
            for pnt in part:
                if pnt:
                    print("{}, {}, {}".format(pnt.X, pnt.Y, pnt.Z))
                    print pnt.touches(g)
                else:
                    # If pnt is None, this represents an interior ring
                    print("Interior Ring:")
            partnum += 1


def thing(fc_stream, fc_contour):
    g_wtc = arcpy.CopyFeatures_management(fc_stream, arcpy.Geometry())
    g_ctr = arcpy.CopyFeatures_management(fc_contour, arcpy.Geometry())

    for g in g_ctr:
        print g.firstPoint, g.lastPoint

    for v in g_wtc[0]:
        print v.X, v.Y, v.Z

##    print g_wtc.JSON






##    arcpy.CreateFeatureclass_management(gdb, fc_result, "POLYLINE", fc_stream)
##    cur = arcpy.da.InsertCursor(fc_result, ["SHAPE@"])
##    array = arcpy.Array()
##    ID = -1
##    for coords in


def main():
    pass

if __name__ == '__main__':
    #read_stream(fc_stream, fc_contour)
    thing(fc_stream, fc_contour)
