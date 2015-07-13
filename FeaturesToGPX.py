'''
Tool Name:  Features to GPX
Source Name: FeaturesToGPX.py
Version: ArcGIS 10.1
Author: Esri

Required Arguments:
         Input Features: path to layer or featureclass on disk
         Output Feature Class: path to GPX which will be created

Description:
         This tool takes input features (layers or featureclass) with either point or line geometry and converts into
         a .GPX file. Points and multipoint features are converted in to WPTs, lines are converted into TRKS. If the
         features conform to a known schema, the output GPX file will honor those fields.
'''

try:
    from xml.etree import cElementTree as ET
except:
    from xml.etree import ElementTree as ET

import arcpy

gpx = ET.Element("gpx", xmlns="http://www.topografix.com/GPX/1/1",
              xalan="http://xml.apache.org/xalan",
              xsi="http://www.w3.org/2001/XMLSchema-instance",
              creator="Esri",
              version="1.0")


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    This function not used, but can be used to create GPX files which are easier to read in a text editor.
    """
    from xml.dom import minidom
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



def featuresToGPX(inputFC, outGPX, pretty=False):
    ''' This is called by the __main__ if run from a tool or at the command line
    '''

    descInput = arcpy.Describe(inputFC)
    if descInput.spatialReference.factoryCode <> 4326:
        arcpy.AddWarning("Input data is not projected in WGS84, features were reprojected on the fly to create the GPX.")

    generatePointsFromFeatures(inputFC , descInput)

    # Write the output GPX file
    try:
        gpxFile = open(outGPX, "w")
        if pretty:
            ET.ElementTree(gpx).write(prettify(gpxFile), encoding="UTF-8", xml_declaration=True)
        else:
            ET.ElementTree(gpx).write(gpxFile, encoding="UTF-8", xml_declaration=True)
    except TypeError:
        arcpy.AddError("Error serializing GPX into the file.")
    finally:
        gpxFile.close()



def generatePointsFromFeatures(inputFC, descInput):

    def attHelper(row):
        # helper function to get/set field attributes for output gpx file

        pnt = row[1].getPart()
        valuesDict["PntX"] = str(pnt.X)
        valuesDict["PntY"] = str(pnt.Y)

        Z = pnt.Z if descInput.hasZ else None
        if Z or ("Elevation" in cursorFields):
            valuesDict["Elevation"] = str(Z) if Z else str(row[fieldNameDict["Elevation"]])  #is not None  <- removed from the if/else
        else:
            valuesDict["Elevation"] = str(0)

        valuesDict["Name"] = row[fieldNameDict["Name"]] if "Name" in fields else " "
        valuesDict["Descript"] = row[fieldNameDict["Descript"]] if "Descript" in fields else " "

        try:
            valuesDict["DateTime"] = row[fieldNameDict["DateTime"]].strftime("%Y-%m-%dT%H:%M:%SZ") #if "DateTime" in fields else " "
        except:
            valuesDict["DateTime"] = " "

        return
    #-------------end helper function-----------------


    def getValuesFromFC( inputFC, cursorFields ):

        previousPartNum = 0
        startTrack = True

        # Loop through all features and parts
        with arcpy.da.SearchCursor(inputFC, cursorFields, spatial_reference="4326", explode_to_points=True) as searchCur:
            for row in searchCur:
                if descInput.shapeType == "Polyline":
                    for part in row:
                        newPart = False
                        if not row[0] == previousPartNum or startTrack == True:
                            startTrack = False
                            newPart = True
                        previousPartNum = row[0]

                        attHelper(row)
                        yield "trk", newPart

                elif descInput.shapeType == "Multipoint" or descInput.shapeType == "Point":
                    #check to see if data was original GPX with "Type" of "TRKPT" or "WPT"
                    trkType = row[fieldNameDict["Type"]].upper() if "Type" in fields else None

                    attHelper(row)

                    if trkType == "TRKPT":
                        newPart = False
                        if previousPartNum == 0:
                            newPart = True
                            previousPartNum = 1

                        yield "trk", newPart

                    else:
                        yield "wpt", None

    #---------end get values function-------------


    # Get list of available fields
    fields = [f.name for f in arcpy.ListFields(inputFC)]
    valuesDict = {"Elevation": 0, "Name": "", "Descript": "", "DateTime": "", "Type": "", "PntX": 0, "PntY": 0}
    fieldNameDict = {"Elevation": 0, "Name": 1, "Descript": 2, "DateTime": 3, "Type": 4, "PntX": 5, "PntY": 6}

    cursorFields = ["OID@", "SHAPE@"]

    for key, item in valuesDict.items():
        if key in fields:
            fieldNameDict[key] = len(cursorFields)  #assign current index
            cursorFields.append(key)   #build up list of fields for cursor
        else:
            fieldNameDict[key] = None

    for index, gpxValues in enumerate(getValuesFromFC(inputFC, cursorFields)):

        if gpxValues[0] == "wpt":
            wpt = ET.SubElement(gpx, 'wpt', {'lon':valuesDict["PntX"], 'lat':valuesDict["PntY"]})
            wptEle = ET.SubElement(wpt, "ele")
            wptEle.text = valuesDict["Elevation"]
            wptTime = ET.SubElement(wpt, "time")
            wptTime.text = valuesDict["DateTime"]
            wptName = ET.SubElement(wpt, "name")
            wptName.text = valuesDict["Name"]
            wptDesc = ET.SubElement(wpt, "desc")
            wptDesc.text = valuesDict["Descript"]

        else:  #TRKS
            if gpxValues[1]:
                # Elements for the start of a new track
                trk = ET.SubElement(gpx, "trk")
                trkName = ET.SubElement(trk, "name")
                trkName.text = valuesDict["Name"]
                trkDesc = ET.SubElement(trk, "desc")
                trkDesc.text = valuesDict["Descript"]
                trkSeg = ET.SubElement(trk, "trkseg")

            trkPt = ET.SubElement(trkSeg, "trkpt", {'lon':valuesDict["PntX"], 'lat':valuesDict["PntY"]})
            trkPtEle = ET.SubElement(trkPt, "ele")
            trkPtEle.text = valuesDict["Elevation"]
            trkPtTime = ET.SubElement(trkPt, "time")
            trkPtTime.text = valuesDict["DateTime"]



if __name__ == "__main__":
    ''' Gather tool inputs and pass them to featuresToGPX(features, output files) '''

    inputFC = arcpy.GetParameterAsText(0)
    outGPX = arcpy.GetParameterAsText(1)
    pretty = arcpy.GetParameterAsText(2)
    featuresToGPX(inputFC, outGPX, pretty=pretty)
