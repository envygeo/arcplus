# Snippets.py

#**** Initialization ****

def GetLibPath():
    """Return location of ArcGIS type libraries as string"""
    # return "C:/Program Files/ArcGIS/com/"
    import _winreg
    keyESRI = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, \
                              "SOFTWARE\\ESRI\\ArcGIS")
    return _winreg.QueryValueEx(keyESRI, "InstallDir")[0] + "com\\"

def GetModule(sModuleName):
    """Import ArcGIS module"""
    from comtypes.client import GetModule
    sLibPath = GetLibPath()
    GetModule(sLibPath + sModuleName)

def GetDesktopModules():
    """Import basic ArcGIS Desktop libraries"""
    GetModule("esriFramework.olb")
    GetModule("esriArcMapUI.olb")

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
    import comtypes.gen.esriSystem as esriSystem
    pInit = NewObj(esriSystem.AoInitialize, \
                   esriSystem.IAoInitialize)
    ProductList = [esriSystem.esriLicenseProductCodeArcEditor, \
                   esriSystem.esriLicenseProductCodeArcView]
    for eProduct in ProductList:
        licenseStatus = pInit.IsProductCodeAvailable(eProduct)
        if licenseStatus != esriSystem.esriLicenseAvailable:
            continue
        licenseStatus = pInit.Initialize(eProduct)
        return (licenseStatus == esriSystem.esriLicenseCheckedOut)
    return False

def GetApp(app="ArcMap"):
    """app must be 'ArcMap' (default) or 'ArcCatalog'\n\
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

def Msg(message="Hello world", title="ARDemo"):
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

def Standalone_OpenGISServer():

    GetModule("esriServer.olb")
    GetModule("esriGeometry.olb")
    import comtypes.gen.esriServer as esriServer
    import comtypes.gen.esriGeometry as esriGeometry

    pServerConn = NewObj(esriServer.GISServerConnection, \
                         esriServer.IGISServerConnection)
    pServerConn.Connect("tuswpesri02")
    pServerManager = pServerConn.ServerObjectManager
    pServerContext = pServerManager.CreateServerContext("", "")

    #pUnk = pServerContext.CreateObject("esriGeometry.Polygon")
    pUnk = pServerContext.CreateObject(CLSID(esriGeometry.Polygon))
    pPtColl = CType(pUnk, esriGeometry.IPointCollection)
    XList = [0, 0, 10, 10]
    YList = [0, 10, 10, 0]
    iCount = 4
    for i in range(iCount):
        #pUnk = pServerContext.CreateObject("esriGeometry.Point")
        pUnk = pServerContext.CreateObject(CLSID(esriGeometry.Point))
        pPoint = CType(pUnk, esriGeometry.IPoint)
        pPoint.PutCoords(XList[i], YList[i])
        pPtColl.AddPoint(pPoint)
    pArea = CType(pPtColl, esriGeometry.IArea)
    print "Area = ", pArea.Area

    pServerContext.ReleaseContext()

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
    
#**** ArcMap ****

def ArcMap_GetSelectedGeometry():

    GetDesktopModules()
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriCarto as esriCarto
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriGeometry as esriGeometry
    pApp = GetApp()
    if not pApp:
        print "We found this spoon, sir."
        return

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

def ArcMap_AddTextElement():

    GetDesktopModules()
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriGeometry as esriGeometry
    import comtypes.gen.esriCarto as esriCarto
    import comtypes.gen.esriDisplay as esriDisplay
    import comtypes.gen.stdole as stdole
    pApp = GetApp()
    pFact = CType(pApp, esriFramework.IObjectFactory)

    # Get midpoint of focus map

    pDoc = pApp.Document
    pMxDoc = CType(pDoc, esriArcMapUI.IMxDocument)
    pMap = pMxDoc.FocusMap
    pAV = CType(pMap, esriCarto.IActiveView)
    pSD = pAV.ScreenDisplay
    pEnv = pAV.Extent
    dX = (pEnv.XMin + pEnv.XMax) / 2
    dY = (pEnv.YMin + pEnv.YMax) / 2
    pUnk = pFact.Create(CLSID(esriGeometry.Point))
    pPt = CType(pUnk, esriGeometry.IPoint)
    pPt.PutCoords(dX, dY)

    # Create text symbol

    pUnk = pFact.Create(CLSID(esriDisplay.RgbColor))
    pColor = CType(pUnk, esriDisplay.IRgbColor)
    pColor.Red = 255
    pUnk = pFact.Create(CLSID(stdole.StdFont))
    pFontDisp = CType(pUnk, stdole.IFontDisp)
    pFontDisp.Name = "Arial"
    pFontDisp.Bold = True
    pUnk = pFact.Create(CLSID(esriDisplay.TextSymbol))
    pTextSymbol = CType(pUnk, esriDisplay.ITextSymbol)
    pTextSymbol.Font = pFontDisp
    pTextSymbol.Color = pColor
    pTextSymbol.Size = 24
    pUnk = pFact.Create(CLSID(esriDisplay.BalloonCallout))
    pTextBackground = CType(pUnk, esriDisplay.ITextBackground)
    pFormattedTS = CType(pTextSymbol, esriDisplay.IFormattedTextSymbol)
    pFormattedTS.Background = pTextBackground

    # Create text element and add it to map

    pUnk = pFact.Create(CLSID(esriCarto.TextElement))
    pTextElement = CType(pUnk, esriCarto.ITextElement)
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
    return

def ArcMap_GetEditWorkspace():

    GetDesktopModules()
    GetModule("esriEditor.olb")
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriEditor as esriEditor
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    pApp = GetApp()
    pID = NewObj(esriSystem.UID, esriSystem.IUID)
    pID.Value = CLSID(esriEditor.Editor)
    pExt = pApp.FindExtensionByCLSID(pID)
    pEditor = CType(pExt, esriEditor.IEditor)
    if pEditor.EditState == esriEditor.esriStateEditing:
        pWS = pEditor.EditWorkspace
        pDS = CType(pWS, esriGeoDatabase.IDataset)
        print "Workspace name: " + pDS.BrowseName
        print "Workspace category: " + pDS.Category

def ArcMap_GetSelectedTable():

    GetDesktopModules()
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriArcMapUI as esriArcMapUI
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    pApp = GetApp()
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

def ArcCatalog_GetSelectedTable():

    GetDesktopModules()
    import comtypes.gen.esriFramework as esriFramework
    import comtypes.gen.esriCatalogUI as esriCatalogUI
    import comtypes.gen.esriCatalog as esriCatalog
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    pApp = GetApp("ArcCatalog")
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

