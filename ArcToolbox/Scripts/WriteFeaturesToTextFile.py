'''----------------------------------------------------------------------------------
 Tool Name:     WriteFeaturesFromTextFile
 Source Name:   WriteFeaturesFromTextFile.py
 Version:       ArcGIS 9.1
 Author:        Environmental Systems Research Institute Inc.
 Required Argumuments:  An input feature class
                        An output text file
                        An input decimal separator character that indicates what character
                        should be used to separate the whole number from its decimal.
 Description:   Writes the features of a feature class out to a text file.
----------------------------------------------------------------------------------'''
import string, os, sys, locale
import arcpy
import arcgisscripting
gp = arcgisscripting.create()
gp.overwriteoutput = 1

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
    gp.AddMessage('Using "%s" for decimal point separator' % sepchar)
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
        arcpy.AddError(msgFieldNotFound + '\n\t%s' % (', '.join(fields)))
    else:
        arcpy.AddMessage('Using "%s" for FeatureID' % f)
    return f

##try:
if len(sys.argv) < 4: raise Exception, msgNotEnoughParams
inputFC = sys.argv[1]
outFile = open(sys.argv[2], "w")

#optional parameters
sepchar = get_sepchar(decimalchar)

inDesc = arcpy.Describe(inputFC)
id_field = validate_id(id_fieldname, inDesc)

inRows = gp.searchcursor(inputFC)
inRow = inRows.next()
outFile.write("//{0}\n".format(inDesc.ShapeType))

while inRow:
    feat = inRow.GetValue(inDesc.ShapeFieldName)
    if inDesc.ShapeType.lower() == "point":
        pnt = feat.getpart()
        outLine = "{0}, {1}, {2}, {3}, {4}\n".format(inRow.GetValue(id_field), pnt.x, pnt.y, pnt.z, pnt.m)
        if sepchar == "": outFile.write(outLine)
        else: outFile.write(outLine.replace(".", sepchar))

    elif inDesc.ShapeType.lower() == "multipoint":
        partnum = 0
        partcount = feat.partcount
        outFile.write("{0}, {1}\n".format(inRow.GetValue(id_field), str(partnum))) # begin new feature
        while partnum < partcount:
            pnt = feat.getpart(partnum)
            outLine = "{0}, {1}, {2}, {3}, {4}\n".format(partnum, pnt.x, pnt.y, pnt.z, pnt.m)
            if sepchar == "": outFile.write(outLine)
            else: outFile.write(outLine.replace(".", sepchar))
            partnum += 1
    else:
        partnum = 0
        partcount = feat.partcount
        while partnum < partcount:
            outFile.write("{0}, {1}\n".format(inRow.GetValue(id_field), str(partnum))) # begin new feature
            part = feat.getpart(partnum)
            part.reset()
            pnt = part.next()
            pnt_count = 0
            while pnt:
                outLine = "{0}, {1}, {2}, {3}\n".format(pnt.x, pnt.y, pnt.z, pnt.m)
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
print gp.GetMessages()

##except Exception, ErrorDesc:
##    gp.AddError(ErrorDesc[0])
##    if outFile: outFile.close()
##    gp.AddError(gp.getmessages(2))
##    print gp.GetMessages()
