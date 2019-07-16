"""
Name:        sdeconn.py
Description: Utility functions for sde connections
Author:      blord-castillo (http://gis.stackexchange.com/users/3386/blord-castillo)

Do on the fly connections in python using Sql Server direct connect only.
Eliminates the problem of database connection files being inconsistent from
machine to machine or user profile to user profile.

Usage:

    import arcpy, sdeconn
    myconnect1 = sdeconn.connect("database1", "server")
    myconnect2 = sdeconn.connect("database2", "server")


Source:
    http://gis.stackexchange.com/questions/16859/define-workspace-for-sde-connection-in-python

"""

# Import system modules
import arcpy, os, sys

def connect(platform, database, server="<default server>", username="<default user>", password="<default password>", version="SDE.DEFAULT", Connection_File_Name):
    # Check if value entered for option
    try:
        #Usage parameters for spatial database connectdaion to upgrade
        service = "sde:{}:{}".format(platform, server)
        account_authentication = 'DATABASE_AUTH'
        version = version.upper()
        database = database.lower()

        # Check if direct connection
        if service.find(":") <> -1:  #This is direct connect
            ServiceConnFileName = service.replace(":", "")
            ServiceConnFileName = ServiceConnFileName.replace(";", "")
            ServiceConnFileName = ServiceConnFileName.replace("=", "")
            ServiceConnFileName = ServiceConnFileName.replace("/", "")
            ServiceConnFileName = ServiceConnFileName.replace("\\", "")
        else:
            arcpy.AddMessage("\n+++++++++")
            arcpy.AddMessage("Exiting!!")
            arcpy.AddMessage("+++++++++")
            sys.exit("\nSyntax for a direct connection in the Service parameter is required for geodatabase upgrade.")

        # Local variables
        Conn_File_NameT = server + "_" + ServiceConnFileName + "_" + database + "_" + username

        if os.environ.get("TEMP") == None:
            temp = "c:\\temp"
        else:
            temp = os.environ.get("TEMP")

        if os.environ.get("TMP") == None:
            temp = "/usr/tmp"
        else:
            temp = os.environ.get("TMP")

        #Connection_File_Name = temp + os.sep + Conn_File_NameT + ".sde"
        #if os.path.isfile(Connection_File_Name):
        #    return Connection_File_Name


        # Check for the .sde file and delete it if present
        arcpy.env.overwriteOutput=True

        # Variables defined within the script; other variable options commented out at the end of the line
        saveUserInfo = "SAVE_USERNAME" #DO_NOT_SAVE_USERNAME
        saveVersionInfo = "SAVE_VERSION" #DO_NOT_SAVE_VERSION


        print "\nCreating ArcSDE Connection File...\n"
        # Process: Create ArcSDE Connection File...
        # Usage: out_folder_path, out_name, server, service, database, account_authentication, username, password, save_username_password, version,   save_version_info
        print temp
        print Conn_File_NameT
        print server
        print service
        print database
        print account_authentication
        print username
        print password
        print saveUserInfo
        print version
        print saveVersionInfo
        arcpy.CreateArcSDEConnectionFile_management(temp,
            Conn_File_NameT,
            server,
            service,
            database,
            account_authentication,
            username,
            password,
            saveUserInfo,
            version,
            saveVersionInfo)
        for i in range(arcpy.GetMessageCount()):
            if "000565" in arcpy.GetMessage(i):   #Check if database connection was successful
                arcpy.AddReturnMessage(i)
                arcpy.AddMessage("\n+++++++++")
                arcpy.AddMessage("Exiting!!")
                arcpy.AddMessage("+++++++++\n")
                sys.exit(3)
            else:
                arcpy.AddReturnMessage(i)
                arcpy.AddMessage("+++++++++\n")
                return Connection_File_Name
    #Check if no value entered for option
    except SystemExit as e:
        print e.code
        return

def get_profile_info():
    '''
    Kudos @Michael-Stimson https://gis.stackexchange.com/a/154572/108
    '''
    d = {}
    d['appdata'] = os.environ.get("APPDATA") # not case sensitive
    d['II']      = arcpy.GetInstallInfo()
    d['version'] = II["Version"]             # Case sensitive
    d['desktop_fld']  = "{0}\\ESRI\\Desktop{1}".format(AppData,Version)
    d['connections'] = "{}\\ArcCatalog".format(d['desktop_fld'])
    return d

def connect_filename(profile, database, username):
    '''Return full path for connection file
     Example:
        "C:\Users\mhwilkie\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\Connection to CSWPROD (mhwilkie).sde"
    '''
    fname = '{0}\\Connection to {1} ({2}).sde'.format(
        profile['connections'],
        database,
        username)
    return fname


def listFcsInGDB():
    ''' set your arcpy.env.workspace to a gdb before calling '''
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            yield os.path.join(arcpy.env.workspace, fds, fc)

if __name__ == '__main__':
    print "started main"
    platform = arcpy.GetParameterAsText(0)
    database = arcpy.GetParameterAsText(1)
    server = arcpy.GetParameterAsText(2)
    username = arcpy.GetParameterAsText(3)
    password = arcpy.GetParameterAsText(4)
    version = arcpy.GetParameterAsText(5)

    if not platform:
        platform = 'Oracle'
    if not version:
        version = "SDE.DEFAULT"

    profile = get_profile_info()

    print "make connection file"
    sde = connect(platform, database, server, username, password, version)

    print sde
    arcpy.env.workspace = sde
    print arcpy.env.workspace

    for fc in listFcsInGDB():
        print fc

    print arcpy.GetMessages()


