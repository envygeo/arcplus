# courtesy of Micheal Jackson
# https://gis.stackexchange.com/questions/1466/using-arcpy-to-get-layer-symbology
import zipfile
from arcpy import mapping
import os
from xml.dom.minidom import parse


class LayerExtras(object):
    """ An object to hold attributes loaded from xml inside the msd."""

    name = ""
    symbologyFieldName = ""


class MxdExtras(dict):
    """ Exposes extra MXD details by raiding an exported msd

        Treat this object as a dictionary with layer name as the key and a custom object
        with desired attributes as the value.
        You must have write access to MXD directory (creates temporary msd file).
        Only layers in the first dataframe are accessed.

    """    

    LYR_NAME_NODE = "Name"
    LYR_SYMBOL_NODE = "Symbolizer"
    LYR_FIELD_NODE = "Field"
    MSD_SUFFIX = "_MxdExtrasTemp.msd"
    MXD_SUFFIX = ".mxd"
    EXCLUDED_FILE_NAMES = ["DocumentInfo.xml", "layers/layers.xml"]
    mxdPath = ""

    def __init__(self, mxdPath):

        self.loadMxdPath(mxdPath)


    def loadMxdPath(self, mxdPath):
        """ Load mxd from file path """

        self.mxdPath = mxdPath.lower()
        mxd = mapping.MapDocument(self.mxdPath)

        msdPath = self.mxdPath.replace(self.MXD_SUFFIX, self.MSD_SUFFIX) 

        # Delete temporary msd if it exists
        if os.path.exists(msdPath):
            os.remove(msdPath)

        mapping.ConvertToMSD(mxd,msdPath)

        zz = zipfile.ZipFile(msdPath)

        for fileName in (fileName for fileName in zz.namelist() if not fileName in self.EXCLUDED_FILE_NAMES):
            dom = parse(zz.open(fileName))
            name, lyr = self.loadMsdLayerDom(dom)
            self[name] = lyr
        del zz
        os.remove(msdPath)

    def loadMsdLayerDom(self, dom):
        """ Load dom created from xml file inside the msd. """

        lyr = LayerExtras()  

        # Layer name
        lyr.name = dom.getElementsByTagName(self.LYR_NAME_NODE)[0].childNodes[0].nodeValue

        # Symbology field name
        symbologyElement = dom.getElementsByTagName(self.LYR_SYMBOL_NODE)[0]
        lyr.symbologyFieldName = symbologyElement.getElementsByTagName(self.LYR_FIELD_NODE)[0].childNodes[0].nodeValue

        return lyr.name, lyr


############
# Test

if __name__ == "__main__":

    mxdPath = r"c:\temp\AmphibianSpeciesRichnessAverageOf30mCells.mxd"

    mxde = MxdExtras(mxdPath)

    for lyr in mxde.itervalues():
        print "Layer Name: ", lyr.name 
        print "Layer Symbology Field Name: ", lyr.symbologyFieldName
        print 