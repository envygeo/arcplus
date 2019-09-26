'''Create personal layer files for all .lyr files from a source folder
with a UNC path.

Designed for use with a password protected geodatabase. Afterwards,
using the personal layer files will skip authentication prompt.

Usage:

    python save-layers-my-credentials.py "[in path]" "[sde file]" "[out path]"

Inputs:
    - UNC path with layer files
        (\\CSWPROD\Layerfiles)
    - SDE Credentials file
        ("%APPDATA%\Esri\Desktop10.6\ArcCatalog\Connection to CSWPROD.sde")
    - Folder to store the result .lyr files
        (C:\users\jonahwhale\Documents\ArcGIS\Layers)

Known Limitations:
    - doesn't handle group layers


Tested with ArcMap 10.6 and Python 2.7 on Win10 x64.

Matt.Wilkie@gov.yk.ca, 2019-07-16
License: X/MIT Open Source
(c) 2019 Environment Yukon
'''
from __future__ import print_function
import os
import sys
import glob
import fnmatch
import arcpy

inpath = arcpy.GetParameterAsText(0)
sdefile  = arcpy.GetParameterAsText(1)
docfolder = arcpy.GetParameterAsText(2)

# hardcoded paths if literal `**DEV` is first parameter
if inpath == '**DEV':
    inpath = r'\\cswprod\Layerfiles'
    docfolder = os.path.join(os.environ['USERPROFILE'],
        r'Documents\ArcGIS\Layers')
    sdefile = os.path.join(os.environ['APPDATA'],
        r"ESRI\Desktop10.7\ArcCatalog\Connection to cswprod.sde")

# verify input path
if not os.path.exists(inpath):
    msg = "*** Input path not found: '{}' ".format(inpath)
    arcpy.AddMessage(msg)
    print('\nUsage: {} "[in UNC path]" "[sde file]" "[out path]"\n'.format(sys.argv[0]))
    sys.exit()

# output
if not os.path.exists(docfolder):
    os.chdir(os.environ['USERPROFILE']) # make sure we start someplace sane
docfolder = os.path.abspath(docfolder)
if not os.path.exists(docfolder):
    os.makedirs(docfolder)

def find_in_catalog(sdefile):
    """Search for sdefile in common Esri catalog connection folders.
    Return full file path or None """
    sdefilepath = None
    dot_sde = os.path.basename(sdefile)
    appdata = os.environ['APPDATA']

    for v in ['10.7', '10.6', '10.5', '10.4', '10.3']:
        fld = os.path.join(appdata, r'ESRI\Desktop'+ v, 'ArcCatalog')
        # print(fld)
        if os.path.exists(fld):
            os.chdir(fld)
            break
    if os.path.exists(dot_sde):
        sdefilepath = os.path.join(fld, dot_sde)

    arcpy.AddMessage("Found: {}".format(sdefilepath))
    return sdefilepath


# verify we can find the .sde connection file
if not os.path.exists(sdefile):
    arcpy.AddMessage("Looking for '{}'".format(sdefile))
    sdefile = find_in_catalog(sdefile)
    if not sdefile:
        msg = "*** SDE file not found"
        arcpy.AddMessage(msg)
        sys.exit()


def get_filenames(inpath, pattern='*.lyr'):
    matches = []
    for root, dirnames, filenames in os.walk(inpath):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

layers = get_filenames(inpath, pattern='*.lyr')

arcpy.AddMessage('IN: {}'.format(inpath))
arcpy.AddMessage('OUT: {}'.format(docfolder))

# Skipped layers
group_layers = []
problem_layers = []

## Main
for L in layers:
    while L:
        try:
            lyr = arcpy.mapping.Layer(L)
        # handle broken layer files (e.g. ArcMap version mismatch).
        except ValueError as e:
            arcpy.AddMessage("*** {}: {}".format(L, e))
            problem_layers.append([L, e])
            break

        if lyr.isGroupLayer:
            group_layers.append(L)
            break

        server = lyr.serviceProperties['Server']

        # Parse in path and filename to remove \\server\share
        # and identify Category and actual layerfile name
        #
        # in = '\\\\cswprod\\Layerfiles\\Administrative Boundaries\\Game Management Areas - 250k.lyr'
        # category = 'Administrative Boundaries'
        # lyrfile = 'Game Management Areas - 250k.lyr'
        x = os.path.splitunc(L)[1]
        x = x.lstrip('\\')
        category, lyrfile = os.path.split(x)
        arcpy.AddMessage('Processing: {}\{}'.format(category, lyrfile))

        # ...\Docs\ArcGIS\Layers\{server}\{category}\{layer.lyr}
        outfolder = os.path.join(docfolder, server, category)
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)

        try:
            lyr.findAndReplaceWorkspacePath('', sdefile, validate=False)

            #full path to output .lyr file
            fname = os.path.join(
                    outfolder,
                    lyr.name)

            lyr.saveACopy(fname)
        except ValueError as e:
            arcpy.AddMessage('*** {}\n\t{}'.format(lyr.name, e))
            problem_layers.append([lyr.name, e])

        del lyr # release from memory
        break


# Report skippped
if group_layers:
    arcpy.AddMessage('\n--- Skipped group layers:\n')
    for s in group_layers:
        arcpy.AddMessage(s)
if problem_layers:
    arcpy.AddMessage('\n--- Unknown problem layers:\n')
    for s in problem_layers:
        arcpy.AddMessage(s)


## --- Notes ---
# "Main" should be wrapped in one or more functions and whole thing run
# from `if __name__ == '__main__':` construct
# That will simplify the While and Break loop exits as well just being
# better code.
#
# Would be nice to handle group layers too.
