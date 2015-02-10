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

import string, os, sys, locale, arcgisscripting
gp = arcgisscripting.create()
gp.overwriteoutput = 1

msgNotEnoughParams = "Incorrect number of input parameters."
msgUseValidDecimalPointSep = "Please use one of the valid decimal point separators."

try:

    if len(sys.argv) < 4: raise Exception, msgNotEnoughParams
    inputFC = sys.argv[1]
    outFile = open(sys.argv[2], "w")
    
    arg3poss = ['default python output', 'locale decimal point', 'comma', 'period', '$sep$']
    if sys.argv[3].lower() not in arg3poss: raise Exception, msgUseValidDecimalPointSep

    if sys.argv[3].lower() == arg3poss[1]:
        locale.setlocale(locale.LC_ALL, '')
        sepchar = locale.localeconv()['decimal_point']
    elif sys.argv[3].lower() == arg3poss[2]: sepchar = ','
    elif sys.argv[3].lower() == arg3poss[3]: sepchar = '.'
    elif sys.argv[3].lower() == arg3poss[4]: sepchar = '$SEP$'
    elif sys.argv[3].lower() == arg3poss[0]: sepchar = ""
    
    inDesc = gp.describe(inputFC)

    inRows = gp.searchcursor(inputFC)
    inRow = inRows.next()
    outFile.write(inDesc.ShapeType + "\n")

    while inRow:
        feat = inRow.GetValue(inDesc.ShapeFieldName)
        if inDesc.ShapeType.lower() == "point":
            pnt = feat.getpart()
            outLine = str(inRow.GetValue(inDesc.OIDFieldName)) + " " + str(pnt.x) + " " + str(pnt.y) + " " + str(pnt.z) + " " + str(pnt.m) + "\n"
            if sepchar == "": outFile.write(outLine)
            else: outFile.write(outLine.replace(".", sepchar))
            
        elif inDesc.ShapeType.lower() == "multipoint":
            partnum = 0
            partcount = feat.partcount
            outFile.write(str(inRow.GetValue(inDesc.OIDFieldName)) + " " + str(partnum) + "\n")
            while partnum < partcount:
                pnt = feat.getpart(partnum)
                outLine = str(partnum) + " " + str(pnt.x) + " " + str(pnt.y) + " " + str(pnt.z) + " " + str(pnt.m) + "\n"
                if sepchar == "": outFile.write(outLine)
                else: outFile.write(outLine.replace(".", sepchar))
                partnum += 1

        else:
            partnum = 0
            partcount = feat.partcount
            while partnum < partcount:
                outFile.write(str(inRow.GetValue(inDesc.OIDFieldName)) + " " + str(partnum) + "\n")
                part = feat.getpart(partnum)
                part.reset()
                pnt = part.next()
                pnt_count = 0
                while pnt:
                    outLine = str(pnt_count) + " " + str(pnt.x) + " " + str(pnt.y) + " " + str(pnt.z) + " " + str(pnt.m) + "\n"
                    if sepchar == "": outFile.write(outLine)
                    else: outFile.write(outLine.replace(".", sepchar))
                    pnt = part.next()
                    pnt_count += 1
                    if not pnt:
                        pnt = part.next()
                        if pnt:
                            outFile.write("InteriorRing\n")

                partnum += 1
        inRow = inRows.next()
    outFile.write("END")
    outFile.flush()
    outFile.close()
    
except Exception, ErrorDesc:
    gp.AddError(ErrorDesc[0])
    if outFile: outFile.close()
    gp.AddError(gp.getmessages(2))
