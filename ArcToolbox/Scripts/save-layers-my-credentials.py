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
    docfolder = r'C:\Users\mhwilkie\Documents\ArcGIS\Layers'
    sdefile = r"C:\Users\mhwilkie\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\Connection to cswprod.sde"

if not os.path.exists(inpath):
    print('\nUsage: {} "[in UNC path]" "[sde file]" "[out path]"\n'.format(sys.argv[0]))
    sys.exit()

if not os.path.exists(sdefile):
    print('\n*** SDE file not found: {}\n'.format(sdefile))
    sys.exit()

if not os.path.exists(docfolder):
    os.makedirs(docfolder)

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
        lyr = arcpy.mapping.Layer(L)

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
# and of course add to a Toolbox for regular users.
