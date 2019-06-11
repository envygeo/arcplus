'''List feature classes and sub-types using attribute domains within gdb

Courtesy of Richard Morgan - https://gis.stackexchange.com/a/217992/108
'''
import arcpy

gdb = arcpy.GetParameterAsText(0)

if not gdb:
    gdb = r"D:\code-mhw-at-yg\arcgiscom_tools\ParseDomainReferences\FGDB1.gdb"

arcpy.env.workspace = gdb

def main(gdb):
    header = "{},{},{},{}".format('Feature_class', 'Subtype', 'Field', 'Domain')
    result = []
    for FC in arcpy.ListFeatureClasses():
        for stcode, stdict in list(arcpy.da.ListSubtypes(FC).items()):
            for stkey in list(stdict.keys()):
                if stkey == 'FieldValues':
                    for field, fieldvals in list(stdict[stkey].items()):
                        if fieldvals[1] is not None:
                            result.append("{},{},{},{}".format(
                                FC,
                                'None' if stcode == 0 else stdict['Name'],
                                field,
                                fieldvals[1].name))
    return result

if __name__ == '__main__':
    rows = main(gdb)
    print(header)
    [print(x) for x in rows]
