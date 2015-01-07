'''Accessing ArcObjects via python and comtypes.

...most definitely a work in progess...


Requirements:
    comtypes module, https://pypi.python.org/pypi/comtypes

Adapted from Mark Cederholm's "Using ArcObjects in Python":
    http://www.pierssen.com/arcgis/misc.htm

Also see:
    http://gis.stackexchange.com/questions/80/how-do-i-access-arcobjects-from-python/
'''

# Snippets.py
# ************************************************
# Updated for ArcGIS 10.2
# ************************************************
# Requires installation of the comtypes package
# Available at: http://sourceforge.net/projects/comtypes/
# Once comtypes is installed, the following modifications
# need to be made for compatibility with ArcGIS 10.2:
# 1) Delete automation.pyc, automation.pyo, safearray.pyc, safearray.pyo
# 2) Edit automation.py
# 3) Add the following entry to the _ctype_to_vartype dictionary (line 794):
#    POINTER(BSTR): VT_BYREF|VT_BSTR,
# ************************************************

#**** Initialization ****

def GetLibPath():
    """Return location of ArcGIS type libraries as string"""
    # This will still work on 64-bit machines because Python runs in 32 bit mode
    import _winreg
    keyESRI = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ESRI\\Desktop10.2")
    return _winreg.QueryValueEx(keyESRI, "InstallDir")[0] + "com\\"

def GetModule(sModuleName):
    """Import ArcGIS module"""
    from comtypes.client import GetModule
    sLibPath = GetLibPath()
    GetModule(sLibPath + sModuleName)

def GetStandaloneModules():
    """Import commonly used ArcGIS libraries for standalone scripts"""
    GetModule("esriSystem.olb")
    GetModule("esriGeometry.olb")
    GetModule("esriCarto.olb")
    GetModule("esriDisplay.olb")
    GetModule("esriGeoDatabase.olb")
    GetModule("esriDataSourcesGDB.olb")
    GetModule("esriDataSourcesFile.olb")
    GetModule("esriOutput.olb")

def GetDesktopModules():
    """Import basic ArcGIS Desktop libraries"""
    GetModule("esriFramework.olb")
    GetModule("esriArcMapUI.olb")
    GetModule("esriArcCatalogUI.olb")

#**** Helper Functions ****

def NewObj(MyClass, MyInterface):
    """Creates a new comtypes POINTER object where\n\
    MyClass is the class to be instantiated,\n\
    MyInterface is the interface to be assigned"""
    from comtypes.client import CreateObject
    try:
        ptr = CreateObject(MyClass, interface=MyInterface)
        return ptr
    except:
        return None

def CType(obj, interface):
    """Casts obj to interface and returns comtypes POINTER or None"""
    try:
        newobj = obj.QueryInterface(interface)
        return newobj
    except:
        return None

def CLSID(MyClass):
    """Return CLSID of MyClass as string"""
    return str(MyClass._reg_clsid_)

def InitStandalone():
    """Init standalone ArcGIS license"""
    # Set ArcObjects version
    import comtypes
    from comtypes.client import GetModule
    g = comtypes.GUID("{6FCCEDE0-179D-4D12-B586-58C88D26CA78}")
    GetModule((g, 1, 0))
    import comtypes.gen.ArcGISVersionLib as esriVersion
    import comtypes.gen.esriSystem as esriSystem
    pVM = NewObj(esriVersion.VersionManager, esriVersion.IArcGISVersion)
    if not pVM.LoadVersion(esriVersion.esriArcGISDesktop, "10.2"):
        return False
    # Get license
    pInit = NewObj(esriSystem.AoInitialize, esriSystem.IAoInitialize)
    ProductList = [esriSystem.esriLicenseProductCodeAdvanced, \
                   esriSystem.esriLicenseProductCodeStandard, \
                   esriSystem.esriLicenseProductCodeBasic]
    for eProduct in ProductList:
        licenseStatus = pInit.IsProductCodeAvailable(eProduct)
        if licenseStatus != esriSystem.esriLicenseAvailable:
            continue
        licenseStatus = pInit.Initialize(eProduct)
        return (licenseStatus == esriSystem.esriLicenseCheckedOut)
    return False

def GetApp(app="ArcMap"):
    """In a standalone script, retrieves the first app session found.\n\
    app must be 'ArcMap' (default) or 'ArcCatalog'\n\
    Execute GetDesktopModules() first"""
    if not (app == "ArcMap" or app == "ArcCatalog"):
        print "app must be 'ArcMap' or 'ArcCatalog'"
        return None
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriCatalogUI as esriCatalogUI
    pAppROT = NewObj(esriFramework.AppROT, esriFramework.IAppROT)
    iCount = pAppROT.Count
    if iCount == 0:
        return None
    for i in range(iCount):
        pApp = pAppROT.Item(i)
        if app == "ArcCatalog":
            if CType(pApp, esriCatalogUI.IGxApplication):
                return pApp
            continue
        if CType(pApp, esriArcMapUI.IMxApplication):
            return pApp
    return None

def GetCurrentApp():
    """Gets an IApplication handle to the current app.\n\
    Must be run inside the app's Python window.\n\
    Execute GetDesktopModules() first"""
    import comtypes.gen.esriFramework as esriFramework
    return NewObj(esriFramework.AppRef, esriFramework.IApplication)

def Msg(message="Hello world", title="PythonDemo"):
    from ctypes import c_int, WINFUNCTYPE, windll
    from ctypes.wintypes import HWND, LPCSTR, UINT
    prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, UINT)
    fn = prototype(("MessageBoxA", windll.user32))
    return fn(0, message, title, 0)

#**** Standalone ****

def Standalone_OpenFileGDB():

    GetStandaloneModules()
    if not InitStandalone():
        print "We've got lumps of it 'round the back..."
        return
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

    sPath = "c:/apps/Demo/Montgomery_full.gdb"
    pWSF = NewObj(esriDataSourcesGDB.FileGDBWorkspaceFactory, \
                  esriGeoDatabase.IWorkspaceFactory)
    pWS = pWSF.OpenFromFile(sPath, 0)
    pDS = CType(pWS, esriGeoDatabase.IDataset)
    print "Workspace name: " + pDS.BrowseName
    print "Workspace category: " + pDS.Category
    return pWS

def Standalone_OpenSDE():

    GetStandaloneModules()
    InitStandalone()
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

    pPropSet = NewObj(esriSystem.PropertySet, esriSystem.IPropertySet)
    pPropSet.SetProperty("SERVER", "sunprod1")
    pPropSet.SetProperty("USER", "/")
    pPropSet.SetProperty("INSTANCE", "sde:oracle10g:/;LOCAL=PRODUCTION_TUCSON")
    pPropSet.SetProperty("AUTHENTICATION_MODE", "OSA")
    pPropSet.SetProperty("VERSION", "SDE.DEFAULT")
    pWSF = NewObj(esriDataSourcesGDB.SdeWorkspaceFactory, \
                  esriGeoDatabase.IWorkspaceFactory)
    pWS = pWSF.Open(pPropSet, 0)
    pDS = CType(pWS, esriGeoDatabase.IDataset)
    print "Workspace name: " + pDS.BrowseName
    print "Workspace category: " + pDS.Category
    return pWS

def Standalone_QueryDBValues():

    GetStandaloneModules()
    InitStandalone()
    import comtypes.gen.esriServer as esriSystem
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

    sPath = "c:/apps/Demo/Montgomery_full.gdb"
    sTabName = "Parcels"
    sWhereClause = "parcel_id = 6358"
    sFieldName = "zoning_s"

    pWSF = NewObj(esriDataSourcesGDB.FileGDBWorkspaceFactory, esriGeoDatabase.IWorkspaceFactory)
    pWS = pWSF.OpenFromFile(sPath, 0)
    pFWS = CType(pWS, esriGeoDatabase.IFeatureWorkspace)
    pTab = pFWS.OpenTable(sTabName)
    pQF = NewObj(esriGeoDatabase.QueryFilter, esriGeoDatabase.IQueryFilter)
    pQF.WhereClause = sWhereClause
    pCursor = pTab.Search(pQF, True)
    pRow = pCursor.NextRow()
    if not pRow:
        print "Query returned no rows"
        return
    Val = pRow.Value(pTab.FindField(sFieldName))
    if Val is None:
        print "Null value"

def Standalone_CreateTable():

    GetStandaloneModules()
    InitStandalone()
    import comtypes.gen.esriServer as esriSystem
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

    sWSPath = "c:/apps/Demo/Temp.gdb"
    sTableName = "Test"
    pWSF = NewObj(esriDataSourcesGDB.FileGDBWorkspaceFactory, \
                  esriGeoDatabase.IWorkspaceFactory)
    pWS = pWSF.OpenFromFile(sWSPath, 0)
    pFWS = CType(pWS, esriGeoDatabase.IFeatureWorkspace)

    pOutFields = NewObj(esriGeoDatabase.Fields, esriGeoDatabase.IFields)
    pFieldsEdit = CType(pOutFields, esriGeoDatabase.IFieldsEdit)
    pFieldsEdit._FieldCount = 2
    pNewField = NewObj(esriGeoDatabase.Field, esriGeoDatabase.IField)
    pFieldEdit = CType(pNewField, esriGeoDatabase.IFieldEdit)
    pFieldEdit._Name = "OBJECTID"
    pFieldEdit._Type = esriGeoDatabase.esriFieldTypeOID
    pFieldsEdit._Field[0] = pNewField
    pNewField = NewObj(esriGeoDatabase.Field, esriGeoDatabase.IField)
    pFieldEdit = CType(pNewField, esriGeoDatabase.IFieldEdit)
    pFieldEdit._Name = "LUMBERJACK"
    pFieldEdit._Type = esriGeoDatabase.esriFieldTypeString
    pFieldEdit._Length = 50
    pFieldsEdit._Field[1] = pNewField
    pOutTable = pFWS.CreateTable(sTableName, pOutFields, \
                                 None, None, "")

    iField = pOutTable.FindField("LUMBERJACK")
    print "'LUMBERJACK' field index = ", iField
    pRow = pOutTable.CreateRow()
    pRow.Value[iField] = "I sleep all night and I work all day"
    pRow.Store()

# ***************************************************************
# NOTE: The following examples, by default, expect to be run
# within ArcMap and ArcCatalog in the Python window.  To run
# them in a standalone session, supply True as the argument.
# ***************************************************************

#**** ArcMap ****

def ArcMap_GetSelectedGeometry(bStandalone=False):

    GetDesktopModules()
    if bStandalone:
        InitStandalone()
        pApp = GetApp()
    else:
        pApp = GetCurrentApp()
    if not pApp:
        print "We found this spoon, sir."
        return
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriCarto as esriCarto
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriGeometry as esriGeometry

    # Get selected feature geometry

    pDoc = pApp.Document
    pMxDoc = CType(pDoc, esriArcMapUI.IMxDocument)
    pMap = pMxDoc.FocusMap
    pFeatSel = pMap.FeatureSelection
    pEnumFeat = CType(pFeatSel, esriGeoDatabase.IEnumFeature)
    pEnumFeat.Reset()
    pFeat = pEnumFeat.Next()
    if not pFeat:
        print "No selection found."
        return
    pShape = pFeat.ShapeCopy
    eType = pShape.GeometryType
    if eType == esriGeometry.esriGeometryPoint:
        print "Geometry type = Point"
    elif eType == esriGeometry.esriGeometryPolyline:
        print "Geometry type = Line"
    elif eType == esriGeometry.esriGeometryPolygon:
        print "Geometry type = Poly"
    else:
        print "Geometry type = Other"
    return pShape

def ArcMap_AddTextElement(bStandalone=False):

    GetDesktopModules()
    import comtypes.gen.esriFramework as esriFramework
    if bStandalone:
        InitStandalone()
        pApp = GetApp()
        pFact = CType(pApp, esriFramework.IObjectFactory)
    else:
        pApp = GetCurrentApp()
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriGeometry as esriGeometry
    import comtypes.gen.esriCarto as esriCarto
    import comtypes.gen.esriDisplay as esriDisplay
    import comtypes.gen.stdole as stdole

    # Get midpoint of focus map

    pDoc = pApp.Document
    pMxDoc = CType(pDoc, esriArcMapUI.IMxDocument)
    pMap = pMxDoc.FocusMap
    pAV = CType(pMap, esriCarto.IActiveView)
    pSD = pAV.ScreenDisplay
    pEnv = pAV.Extent
    dX = (pEnv.XMin + pEnv.XMax) / 2
    dY = (pEnv.YMin + pEnv.YMax) / 2
    if bStandalone:
        pUnk = pFact.Create(CLSID(esriGeometry.Point))
        pPt = CType(pUnk, esriGeometry.IPoint)
    else:
        pPt = NewObj(esriGeometry.Point, esriGeometry.IPoint)
    pPt.PutCoords(dX, dY)

    # Create text symbol

    if bStandalone:
        pUnk = pFact.Create(CLSID(esriDisplay.RgbColor))
        pColor = CType(pUnk, esriDisplay.IRgbColor)
    else:
        pColor = NewObj(esriDisplay.RgbColor, esriDisplay.IRgbColor)
    pColor.Red = 255
    if bStandalone:
        pUnk = pFact.Create(CLSID(stdole.StdFont))
        pFontDisp = CType(pUnk, stdole.IFontDisp)
    else:
        pFontDisp = NewObj(stdole.StdFont, stdole.IFontDisp)
    pFontDisp.Name = "Arial"
    pFontDisp.Bold = True
    if bStandalone:
        pUnk = pFact.Create(CLSID(esriDisplay.TextSymbol))
        pTextSymbol = CType(pUnk, esriDisplay.ITextSymbol)
    else:
        pTextSymbol = NewObj(esriDisplay.TextSymbol, esriDisplay.ITextSymbol)
    pTextSymbol.Font = pFontDisp
    pTextSymbol.Color = pColor
    pTextSymbol.Size = 24
    if bStandalone:
        pUnk = pFact.Create(CLSID(esriDisplay.BalloonCallout))
        pTextBackground = CType(pUnk, esriDisplay.ITextBackground)
    else:
        pTextBackground = NewObj(esriDisplay.BalloonCallout, esriDisplay.ITextBackground)
    pFormattedTS = CType(pTextSymbol, esriDisplay.IFormattedTextSymbol)
    pFormattedTS.Background = pTextBackground

    # Create text element and add it to map

    if bStandalone:
        pUnk = pFact.Create(CLSID(esriCarto.TextElement))
        pTextElement = CType(pUnk, esriCarto.ITextElement)
    else:
        pTextElement = NewObj(esriCarto.TextElement, esriCarto.ITextElement)
    pTextElement.Symbol = pTextSymbol
    pTextElement.Text = "Wink, wink, nudge, nudge,\nSay no more!"
    pElement = CType(pTextElement, esriCarto.IElement)
    pElement.Geometry = pPt

    pGC = CType(pMap, esriCarto.IGraphicsContainer)
    pGC.AddElement(pElement, 0)
    pGCSel = CType(pMap, esriCarto.IGraphicsContainerSelect)
    pGCSel.SelectElement(pElement)
    iOpt = esriCarto.esriViewGraphics + \
           esriCarto.esriViewGraphicSelection
    pAV.PartialRefresh(iOpt, None, None)

    # Get element width

    iCount = pGCSel.ElementSelectionCount
    pElement = pGCSel.SelectedElement(iCount - 1)
    pEnv = NewObj(esriGeometry.Envelope, esriGeometry.IEnvelope)
    pElement.QueryBounds(pSD, pEnv)
    print "Width = ", pEnv.Width

def ArcMap_GetEditWorkspace(bStandalone=False):

    GetDesktopModules()
    if bStandalone:
        InitStandalone()
        pApp = GetApp()
    else:
        pApp = GetCurrentApp()
    GetModule("esriEditor.olb")
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriEditor as esriEditor
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    pID = NewObj(esriSystem.UID, esriSystem.IUID)
    pID.Value = CLSID(esriEditor.Editor)
    pExt = pApp.FindExtensionByCLSID(pID)
    pEditor = CType(pExt, esriEditor.IEditor)
    if pEditor.EditState == esriEditor.esriStateEditing:
        pWS = pEditor.EditWorkspace
        pDS = CType(pWS, esriGeoDatabase.IDataset)
        print "Workspace name: " + pDS.BrowseName
        print "Workspace category: " + pDS.Category
    return

def ArcMap_GetSelectedTable(bStandalone=False):

    GetDesktopModules()
    if bStandalone:
        InitStandalone()
        pApp = GetApp()
    else:
        pApp = GetCurrentApp()
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    pDoc = pApp.Document
    pMxDoc = CType(pDoc, esriArcMapUI.IMxDocument)
    pUnk = pMxDoc.SelectedItem
    if not pUnk:
        print "Nothing selected."
        return
    pTable = CType(pUnk, esriGeoDatabase.ITable)
    if not pTable:
        print "No table selected."
        return
    pDS = CType(pTable, esriGeoDatabase.IDataset)
    print "Selected table: " + pDS.Name

#**** ArcCatalog ****

def ArcCatalog_GetSelectedTable(bStandalone=False):

    GetDesktopModules()
    if bStandalone:
        InitStandalone()
        pApp = GetApp("ArcCatalog")
    else:
        pApp = GetCurrentApp()
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriCatalogUI as esriCatalogUI
    import comtypes.gen.esriCatalog as esriCatalog
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    pGxApp = CType(pApp, esriCatalogUI.IGxApplication)
    pGxObj = pGxApp.SelectedObject
    if not pGxObj:
        print "Nothing selected."
        return
    pGxDS = CType(pGxObj, esriCatalog.IGxDataset)
    if not pGxDS:
        print "No dataset selected."
        return
    eType = pGxDS.Type
    if not (eType == esriGeoDatabase.esriDTFeatureClass or eType == esriGeoDatabase.esriDTTable):
        print "No table selected."
        return
    pDS = pGxDS.Dataset
    pTable = CType(pDS, esriGeoDatabase.ITable)
    print "Selected table: " + pDS.Name

