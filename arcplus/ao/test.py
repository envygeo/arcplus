import os
import comtypes.client
from arcplus import ao


def GenerateComWrappers(com_dir):
    """Generate wrappers for every ESRI com lib.

    com_dir = r'C:\Program Files (x86)\ArcGIS\Desktop10.0\com'

    Results go to "PYTHONPATH\\lib\site-packages\comtypes\gen"

    GetModule skips existing results.

    Courtesy of Frank Perks, "ArcMap 10, ArcObjects, and Python:  very cool, but
    help with a couple of problems?" -- https://geonet.esri.com/thread/15228
    """
    print 'Generating wrappers for every ESRI com lib in:', com_dir
    coms = [os.path.join(com_dir, x) for x in os.listdir(com_dir) if os.path.splitext(x)[1].upper() == '.OLB']

    success = []
    failed = {}
    for c in coms:
        print '---', c
        try:
            comtypes.client.GetModule(c)
            success.append(c)
        except AttributeError as e:
            failed[c] = e

    print '\n!!! Succeeded or wrapper already exists:'
    for s in success: print s

    print '\n*** Failed:'
    for k in failed.keys():
        print '{0} -- AttributeError: {1}'.format(k, failed[k])

def Example():
    # initialise the com libraries
    ##from comtypes.client import GetModule, CreateObject
    m = ao.GetModule(libPath + "esriGeometry.olb")
    ao.InitStandalone()
    p = ao.CreateObject(m.Point, interface=m.IPoint)
    p.PutCoords(2,3)
    print p.X, p.Y

if __name__ == '__main__':
    libPath = ao.GetLibPath()

    GenerateComWrappers(libPath)












