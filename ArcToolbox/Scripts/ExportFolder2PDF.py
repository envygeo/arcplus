#Export a folder of maps to PDFs at their Map Document set sizes
#Written using ArcGIS 10 and Python 2.6.5
#by: Guest
# https://gis.stackexchange.com/questions/7147/how-to-batch-export-mxd-to-pdf-files

import arcpy, os

#Read input parameter from user.
path = arcpy.GetParameterAsText(0)

#Write MXD names in folder to txt log file.
writeLog=open(path+"\FileListLog.txt","w")
for fileName in os.listdir(path):
    fullPath = os.path.join(path, fileName)
    if os.path.isfile(fullPath):
        basename, extension = os.path.splitext(fullPath)
        if extension == ".mxd":
            writeLog.write(fullPath+"\n")
            mxd = arcpy.mapping.MapDocument(fullPath)
            print fileName + "\n"
del mxd
print "Done"
writeLog.close()


exportPath =arcpy.GetParameterAsText(1)
MXDread=open(path+"\FileListLog.txt","r")
for line in MXDread:
    #Strip newline from line.
    line=line.rstrip('\n')
    if os.path.isfile(line):
        basename, extension = os.path.splitext(line)
        newName=basename.split('\\')[-1]
        if extension.lower() == ".mxd":
            print "Basename:" +newName
            mxd = arcpy.mapping.MapDocument(line)
            newPDF=exportPath+"\\"+newName+".pdf"
            print newPDF
            arcpy.mapping.ExportToPDF(mxd,newPDF)
            print line + "Export Done"
MXDread.close()
item=path+"\FileListLog.txt"
os.remove(item)
del mxd