'''List feature classes, sub-types and tables using attribute domains within gdb

Adapted from Richard Morgan - https://gis.stackexchange.com/a/217992/108
'''
import arcpy

gdb = arcpy.GetParameterAsText(0)

if not gdb:
    gdb = r"D:\code-mhw-at-yg\arcgiscom_tools\ParseDomainReferences\FGDB1.gdb"

arcpy.env.workspace = gdb

header = "{},{},{},{}".format('Item', 'Subtype', 'Field', 'Domain')
def main(gdb):
    '''Returns nested lists of Feature Class or Table, then active domains
    within the FC/Table'''
    result = []
    for FC in arcpy.ListFeatureClasses():
        result.append(find_in_use_domains(FC))
    for TB in arcpy.ListTables():
        result.append(find_in_use_domains(TB))
    return result

def find_in_use_domains(item):
    '''Return field names with active domains in the feature class or table'''
    result = []
    for stcode, stdict in list(arcpy.da.ListSubtypes(item).items()):
        for stkey in list(stdict.keys()):
            if stkey == 'FieldValues':
                for field, fieldvals in list(stdict[stkey].items()):
                    if fieldvals[1] is not None:
                        result.append("{},{},{},{}".format(
                            item,
                            'None' if stcode == 0 else stdict['Name'],
                            field,
                            fieldvals[1].name))
    return result


if __name__ == '__main__':
    rows = main(gdb)
    print(header)
    for r in rows:
        if r:
            [print(x) for x in r]
