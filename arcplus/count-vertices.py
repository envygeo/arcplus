import os
import arcpy

workspace = arcpy.GetParameterAsText(0)
if not workspace:
    workspace = 'Z:\V5\ENV_250k.gdb'

def count_vertices(fc, table):
    '''Count vertices in Feature Class, insert to dictionary named "table"'''
    # Adapted from Alex Tereshenkov (@alex-tereshenkov)
    # https://gis.stackexchange.com/questions/84796/extracting-number-of-vertices-in-each-polygon
    features = [feature[0] for feature in arcpy.da.SearchCursor(fc,"SHAPE@")]
    count_vertices = sum([f.pointCount-f.partCount for f in features])
    #arcpy.AddMessage("{:60}\t:\t{:>,}".format(fc, count_vertices))
    table[fc] = count_vertices

def print_report(table):
    '''Print dictionary as table
    (Naive, paths longer than X characters mess up the table)'''
    print "{:60}\t:\t{:>12}".format('-' * 60, '-' * 12)
    print "{:60}\t:\t{:>12}".format('Feature Class', 'Vertices')
    print "{:60}\t:\t{:>12}".format('-' * 60, '-' * 12)
    for k,v in table.items():
        print "{:60}\t:\t{:>12,}".format(k,v)    


def get_feature_classes(workspace):
    '''Return list of all feature classes under Workspace (recursive)'''
    # # https://gis.stackexchange.com/questions/5893/listing-all-feature-classes-in-file-geodatabase-including-within-feature-datase
    feature_classes = []
    walk = arcpy.da.Walk(workspace, datatype="FeatureClass")
    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            feature_classes.append(os.path.join(dirpath, filename))
    return feature_classes


table = {}
for fc in feature_classes:
    count_vertices(fc,table)

print_report(table)
