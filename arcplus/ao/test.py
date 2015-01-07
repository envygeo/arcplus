from arcplus import ao

libPath = ao.GetLibPath()

#ao.GenerateComWrappers(libPath)

# initialise the com libraries
from comtypes.client import GetModule, CreateObject
m = GetModule(libPath + "esriGeometry.olb")
ao.InitStandalone()
p = CreateObject(m.Point, interface=m.IPoint)
p.PutCoords(2,3)
print p.X, p.Y


##def GenerateComWrappers(ComDir):
##    """Generate wrappers for every ESRI com lib.
##
##    Courtesy of Frank Perks, "ArcMap 10, ArcObjects, and Python:  very cool, but
##    help with a couple of problems?" -- https://geonet.esri.com/thread/15228
##    """
##    import os
##    import comtypes.client
##    # change com_dir to whatever it is for you
##    #com_dir = r'C:\Program Files (x86)\ArcGIS\Desktop10.0\com'
##    com_dir = ComDir
##    coms = [os.path.join(com_dir, x) for x in os.listdir(com_dir) if os.path.splitext(x)[1].upper() == '.OLB']
##    map(comtypes.client.GetModule, coms)
