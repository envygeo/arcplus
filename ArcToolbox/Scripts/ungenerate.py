''' ungenerate.py - write features to ArcInfo GENERATE text file format.

Arguments:
    - input feature class
    - output file name
    - decimal separator character (comma, period, system locale)
    - field to use for ID of each feature (optional)

Matt.Wilkie@gov.yk.ca, 2015-Feb-13

Tested with ArcGIS 10.3.

Adapted from "WriteFeaturesFromTextFile.py" in the Samples Toolbox distributed
by Environmental Systems Research Institute Inc. (Esri) in ArcGIS 9.x.
http://webhelp.esri.com/arcgisdesktop/9.3/index.cfm?TopicName=An_overview_of_the_Samples_toolbox
'''
import string, os, sys, locale
import arcpy

inputFC = arcpy.GetParameterAsText(0)
outFile = arcpy.GetParameterAsText(1)
decimalchar = arcpy.GetParameterAsText(2)
id_fieldname = arcpy.GetParameterAsText(3)

msgNotEnoughParams = "Incorrect number of input parameters."
msgUseValidDecimalPointSep = "Please use one of the valid decimal point separators."
msgFieldNotFound = 'ID field not found. Specify "#" for default or one of:'

def get_sepchar(arg):
    '''Return decimal point separator to use'''
    default_seps = ['default python output', 'locale decimal point', '#']
    valid_seps = {'comma':',', 'period':'.', '$sep$':'$SEP$'}
    for i in default_seps:
        valid_seps[i] = 'locale default'

    arg = arg.lower()
    if arg not in valid_seps:
        raise Exception, msgUseValidDecimalPointSep + str(valid_seps.keys())

    if arg in default_seps:
        locale.setlocale(locale.LC_ALL, '')
        sepchar = locale.localeconv()['decimal_point']
    elif arg in valid_seps:
        sepchar = valid_seps[arg]
    ##elif arg == arg3poss[0]: sepchar = "" # is this ever valid? disabling for now.
    arcpy.AddMessage('Using "{0}" for decimal point separator'.format(sepchar))
    return sepchar

def validate_id(fieldname, desc):
    '''Validate 'fieldname' to use for UNGENERATE Feature ID label.

    '#' means use defined ObjectID or first field.

    field = string
    desc = feature class describe object

    Returns 'field' as string or False
    '''
    fields = [f.name.upper() for f in desc.fields]
    f = None
    if fieldname.upper() in fields:
       f = fieldname
    else:
        if fieldname == '#':
            try:
                f = desc.OIDFieldName
            except:
                f = fields[0]
    if not f:
        arcpy.AddError(msgFieldNotFound + '\n\t{0}'.format(', '.join(fields)))
    else:
        arcpy.AddMessage('Using "{0}" for FeatureID'.format(f))
    return f

if len(sys.argv) < 4: raise Exception, msgNotEnoughParams
inputFC = sys.argv[1]
outFile = open(sys.argv[2], "w")

#optional parameters
sepchar = get_sepchar(decimalchar)

arcpy.AddMessage('\n--- {0}'.format(inputFC))
inDesc = arcpy.Describe(inputFC)
id_field = validate_id(id_fieldname, inDesc)

inRows = arcpy.SearchCursor(inputFC)
inRow = inRows.next()

outFile.write("//{0}\n".format(inDesc.ShapeType))

while inRow:
    feat = inRow.getValue(inDesc.ShapeFieldName)
    if inDesc.ShapeType.lower() == "point":
        pnt = feat.getPart()
        outLine = "{0}, {1}, {2}, {3}, {4}\n".format(inRow.getValue(id_field), pnt.X, pnt.Y, pnt.Z, pnt.M)
        if sepchar == "": outFile.write(outLine)
        else: outFile.write(outLine.replace(".", sepchar))

    elif inDesc.ShapeType.lower() == "multipoint":
        partnum = 0
        partcount = feat.partCount
        outFile.write("{0}, {1}\n".format(inRow.getValue(id_field), str(partnum))) # begin new feature
        while partnum < partcount:
            pnt = feat.getPart(partnum)
            outLine = "{0}, {1}, {2}, {3}, {4}\n".format(partnum, pnt.X, pnt.Y, pnt.Z, pnt.M)
            if sepchar == "": outFile.write(outLine)
            else: outFile.write(outLine.replace(".", sepchar))
            partnum += 1
    else:
        partnum = 0
        partcount = feat.partCount
        while partnum < partcount:
            outFile.write("{0}, {1}\n".format(inRow.getValue(id_field), str(partnum))) # begin new feature
            part = feat.getPart(partnum)
            part.reset()
            pnt = part.next()
            pnt_count = 0
            while pnt:
                outLine = "{0}, {1}, {2}, {3}\n".format(pnt.X, pnt.Y, pnt.Z, pnt.M)
                if sepchar == "": outFile.write(outLine)
                else: outFile.write(outLine.replace(".", sepchar))
                pnt = part.next()
                pnt_count += 1
                if not pnt:
                    pnt = part.next()
                    if pnt:
                        outFile.write("InteriorRing\n")
            outFile.write("END\n") # end feature
            partnum += 1
    inRow = inRows.next()
outFile.write("END")
outFile.flush()
outFile.close()
arcpy.AddMessage('Wrote {0}'.format(outFile.name))
print arcpy.GetMessages()
