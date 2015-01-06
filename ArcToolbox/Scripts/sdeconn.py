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

def connect(database, server="<default server>", username="<default user>", password="<default password>", version="SDE.DEFAULT"):
    # Check if value entered for option
    try:
        #Usage parameters for spatial database connection to upgrade
        service = "sde:sqlserver:" + server
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

        Connection_File_Name = temp + os.sep + Conn_File_NameT + ".sde"
        if os.path.isfile(Connection_File_Name):
            return Connection_File_Name

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
        arcpy.CreateArcSDEConnectionFile_management(temp, Conn_File_NameT, server, service, database, account_authentication, username, password, saveUserInfo, version, saveVersionInfo)
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
