'''
Tool Name:  GPX to Features
Source Name: GPXtoFeaturesXY.py
Version: ArcGIS 10.1-env.2
Author: ESRI

Required Arguments:
         Input GPX File: path to GPX file
         Output Feature Class: path to featureclass which will be created

Description:
         This tool takes a .GPX file (a common output from handheld GPS receivers). The tool will parse all points
         which particpate as either a waypoint (WPT) or inside a track as a track point (TRKPT). The output feature class
         will create fields for the shape, time, and elevation and description.

Modified by Matt.Wilkie@gov.yk.ca for Environment Yukon:

  + 2013-May-16: add X and Y as attribute fields in addition to geometry fields
  * 2014-May-22: sync with upstream 10.2.2 changes (more track info)
'''

# Imports
try:
  from xml.etree import cElementTree as ElementTree
except:
  from xml.etree import ElementTree

import arcpy
import arcpy.da as da
import os
import numpy


def gpxToPoints(gpxfile, outFC):
    ''' This is called by the __main__ if run from a tool or at the command line
    '''

    # Set the tree to the input GPX file
    #
    tree = ElementTree.parse(gpxfile)

    global TOPOGRAFIX_NS
    TOPOGRAFIX_NS = ''
    TOPOGRAFIX_NS10 = './/{http://www.topografix.com/GPX/1/0}'
    TOPOGRAFIX_NS11 = './/{http://www.topografix.com/GPX/1/1}'

    badPt = 0

    # Inspection of the GPX file will yield and set the appropraite namespace. If 1.0 or 1.1
    # is not found, empty output will be generated
    #
    for TRKorWPT in ['wpt', 'trk', 'rte']:   
        if tree.findall(TOPOGRAFIX_NS10 + TRKorWPT):
            TOPOGRAFIX_NS = TOPOGRAFIX_NS10
        elif tree.findall(TOPOGRAFIX_NS11 + TRKorWPT):
            TOPOGRAFIX_NS = TOPOGRAFIX_NS11


    if TOPOGRAFIX_NS == '':
            arcpy.AddIDMessage("Warning", 1202)

    # Create the output feature class in WGS84
    #
    arcpy.CreateFeatureclass_management(os.path.dirname(outFC), os.path.basename(outFC), 'POINT', '', 'DISABLED', 'ENABLED', 4326)


    # Join fields to the feature class, using ExtendTable
    inarray = numpy.array([],
                      numpy.dtype([('intfield', numpy.int32),
                                   ('Name', '|S'),
                                   ('Descript', '|S'),
                                   ('Type', '|S'),
                                   ('Comment', '|S'),
                                   ('Symbol', '|S'),
                                   ('DateTimeS', '|S'),                                   
                                   ('Elevation', numpy.float),
                                   ('X', numpy.float),
                                   ('Y', numpy.float),
                                   ]))
    
    arcpy.da.ExtendTable(outFC, "OID@", inarray, "intfield")


    rowsDA = da.InsertCursor(outFC, ['Name', 'Descript', 'Type', 'Comment', 'Symbol', 'DateTimeS', 'Elevation', 'X', 'Y', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@Z'])


    # Loop over each point in the tree and put the information inside a new row
    #
    for index, trkPoint in enumerate(GeneratePointFromXML(tree)):
        if trkPoint.asPoint() is not None:
            rowsDA.insertRow([trkPoint.name, trkPoint.desc, trkPoint.gpxtype, trkPoint.cmt, trkPoint.sym, 
                              trkPoint.t, trkPoint.z, trkPoint.x, trkPoint.y, trkPoint.x, trkPoint.y, trkPoint.z])
        else:
            badPt +=1


    if badPt > 0:
        arcpy.AddIDMessage("WARNING", 1201, badPt, index + 1)

        
    if tree:
        del tree
    if rowsDA:
        del rowsDA        
       
        
    # Try to create a DateTime field of Date-type for non-shapefile output
    #
    if not outFC.lower().endswith(".shp"):
      try:
        arcpy.ConvertTimeField_management(outFC, 'DateTimeS', 'yyyy-MM-ddTHH:mm:ssZ', "DateTime")

      except:
        arcpy.AddIDMessage("WARNING", 1227)

        try:
          arcpy.DeleteField_management(outFC, "DateTime")
        except:
          pass



class classGPXPoint(object):
    ''' Object to gather GPX information '''

    name = ''
    desc = ''
    cmt = ''
    sym = ''
    gpxtype = 'WPT'
    x = None
    y = None
    z = 0
    t = ''


    def __init__(self, node, gpxtype, name, desc, cmt, sym):
        self.name = name
        self.desc = desc
        self.cmt = cmt
        self.sym = sym
        self.gpxtype = gpxtype
        self.y = node.attrib.get('lat')
        self.x = node.attrib.get('lon')
        self.z = node.find(TOPOGRAFIX_NS + 'ele').text if node.find(TOPOGRAFIX_NS + 'ele') is not None else '0.0'
        self.t = node.find(TOPOGRAFIX_NS + 'time').text or '' if node.find(TOPOGRAFIX_NS + 'time') is not None else ''


    def asPoint(self):
        ''' Try to float X/Y. If conversion to a float fails, the X/Y is not valid and return NONE. '''

        try:
            self.x = float(self.x.replace(',','.'))
            self.y = float(self.y.replace(',','.')) 
            self.z = float(self.z.replace(',','.'))
            
            return self.x, self.y, self.z        

        except:
            return None



def GeneratePointFromXML(tree):
    ''' 1) Inspect the tree for either TRK or WPT
           TRK's have a sub node of TRKPT which are examined.
        2) Yield the information back to insertcursor from the classGPXPoint object.    '''

    def _getNameDesc(node):
        name = node.find(TOPOGRAFIX_NS + 'name').text or '' if node.find(TOPOGRAFIX_NS + 'name') is not None else ''
        desc = node.find(TOPOGRAFIX_NS + 'desc').text or '' if node.find(TOPOGRAFIX_NS + 'desc') is not None else ''
        cmt = node.find(TOPOGRAFIX_NS + 'cmt').text or '' if node.find(TOPOGRAFIX_NS + 'cmt') is not None else ''
        sym = node.find(TOPOGRAFIX_NS + 'sym').text or '' if node.find(TOPOGRAFIX_NS + 'sym') is not None else ''
        return name, desc, cmt, sym

    for node in tree.findall(TOPOGRAFIX_NS + 'trk'):
        name, desc, cmt, sym = _getNameDesc(node)
        for node in node.findall(TOPOGRAFIX_NS + 'trkpt') :
            yield (classGPXPoint(node, 'TRKPT', name, desc, cmt, sym))
         
    for node in tree.findall(TOPOGRAFIX_NS + 'rte'):
        name, desc, cmt, sym = _getNameDesc(node)
        for node in node.findall(TOPOGRAFIX_NS + 'rtept') :
            yield (classGPXPoint(node, 'RTEPT', name, desc, cmt, sym))

    for node in tree.findall(TOPOGRAFIX_NS + 'wpt'):
        name, desc, cmt, sym = _getNameDesc(node)
        yield classGPXPoint(node, 'WPT', name, desc, cmt, sym)


if __name__ == "__main__":
    ''' Gather tool inputs and pass them to gpxToPoints(file, outputFC) '''

    gpx = arcpy.GetParameterAsText(0)
    outFC = arcpy.GetParameterAsText(1)
    gpxToPoints(gpx, outFC)
