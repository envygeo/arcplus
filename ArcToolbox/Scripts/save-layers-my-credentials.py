# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "arcpy",
# ]
# ///

r'''Create personal layer files for all .lyr files from a source folder
with a UNC path.

DRAFT: in process of migrating to python 3 and ArcPro.

Designed for use with a password protected geodatabase. Afterwards,
using the personal layer files will skip authentication prompt.

Usage:

    python save-layers-my-credentials.py "[in path]" "[sde file]" "[out path]"

Inputs:
    - UNC path with layer files
        (\\CSWPROD\Layerfiles)
    - SDE Credentials file
        ("%LOCALAPPDATA%\ESRI\ArcGISPro\Favorites\Connection to CSWPROD.sde")
    - Folder to store the result .lyr files
        (C:\users\jonahwhale\Documents\ArcGIS\Layers)

Known Limitations:
    - doesn't handle group layers

Tested with ArcGIS Pro v3.2 and Python 3.9 on Win10 x64.

Matt.Wilkie@gov.yk.ca, 2024-02-xx
License: X/MIT Open Source
(c) 2019-2024 Environment Yukon
'''
# from __future__ import print_function
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
    inpath = r'\\cswprod\ProLayerfiles'
    docfolder = os.path.join(os.environ['USERPROFILE'],
        r'Documents\ArcGIS\Layers')
    sdefile = os.path.join(os.environ['LOCALAPPDATA'],
        r"ESRI\ArcGISPro\Favorites\Connection to cswprod.sde")

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
    # appdata = os.environ['APPDATA']
    localappdata = os.environ['LOCALAPPDATA']
    if os.path.exists(localappdata):
        os.chdir(localappdata)
    if os.path.exists(dot_sde):
        sdefilepath = os.path.join(localappdata, dot_sde)

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

# Establish database connection first
try:
    arcpy.AddMessage(f"Establishing database connection using: {sdefile}")
    workspace = arcpy.Describe(sdefile)
    connection_props = workspace.connectionProperties
    arcpy.AddMessage("Database connection established")
except Exception as e:
    arcpy.AddMessage(f"Failed to establish database connection: {e}")
    sys.exit(1)

def get_filenames(inpath, pattern='*.lyr?'):
    matches = []
    for root, dirnames, filenames in os.walk(inpath):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

layers = get_filenames(inpath, pattern='*.lyr?')

arcpy.AddMessage('IN: {}'.format(inpath))
arcpy.AddMessage('OUT: {}'.format(docfolder))

arcpy.AddMessage(f"Found {len(layers)} layer files to process")

# Skipped layers
group_layers = []
problem_layers = []

## Main
for L in layers:
    while L:
        try:
            arcpy.AddMessage(f"\nProcessing layer: {L}")
            
            # Parse layer path and get output location using modern path handling
            # Convert Windows path to parts and remove empty elements
            path_parts = [p for p in L.split('\\') if p]
            
            # Get category (parent folder) and filename
            category = path_parts[-2]  # Parent folder name
            lyrfile = path_parts[-1]   # Filename
            
            arcpy.AddMessage('Processing: {}\{}'.format(category, lyrfile))

            # Create output folder structure
            outfolder = os.path.join(docfolder, category)
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)
                
            # Create output layer path
            outfile = os.path.join(outfolder, os.path.basename(L))
            
            # Copy the connection file to temp
            temp_connection = os.path.join(os.environ['TEMP'], "temp_connection.sde")
            arcpy.Copy_management(sdefile, temp_connection)
            
            try:
                # Set the workspace
                arcpy.env.workspace = temp_connection
                
                # Create new layer file
                desc = arcpy.Describe(L)
                if hasattr(desc, 'dataElement'):
                    data_source = desc.dataElement.catalogPath
                    arcpy.AddMessage(f"Data source: {data_source}")
                    
                    # Create new layer with the connection
                    arcpy.management.MakeFeatureLayer(
                        in_features=data_source,
                        out_layer="temp_layer"
                    )
                    
                    # Save the layer file
                    arcpy.management.SaveToLayerFile(
                        in_layer="temp_layer",
                        out_layer=outfile,
                        is_relative_path="ABSOLUTE"
                    )
                    
                    arcpy.AddMessage(f"Successfully saved: {outfile}")
                else:
                    arcpy.AddMessage(f"*** Could not get data source for layer: {L}")
                    problem_layers.append([L, "No data source found"])
                
            finally:
                # Cleanup
                if os.path.exists(temp_connection):
                    os.remove(temp_connection)
                
            break

        except Exception as e:
            arcpy.AddMessage(f"*** Error processing {L}: {str(e)}")
            problem_layers.append([L, str(e)])
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
