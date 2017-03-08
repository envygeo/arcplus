[{"Data Type":"Address locator","Description":"A dataset, used for geocoding, that stores the address\nattributes, associated indexes, and rules that define the
process for translating nonspatial descriptions of places to
spatial data. [.loc]","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEAddressLocator"},
{"Data Type":"Address locator style","Description":"A template on which to base the new address locator. [.lot]","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"GPAddressLocatorStyle"},
{"Data Type":"Analysis cell size","Description":"The cell size used by raster tools.","String Syntax1":"cellSize | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPAnalysisCellSize"},
{"Data Type":"Any value","Description":"A data type that accepts any value.","String Syntax1":"any value","Scripting Object3":". _ .","ArcObjects":"GPType [abstract datatype]"},
{"Data Type":"ArcMap Document","Description":"A file that contains one map, its layout, and its associated\nlayers, tables, charts, and reports. [.mxd]","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEMapDocument"},
{"Data Type":"Area units","Description":"An areal unit type and value such as square meter or\nacre.","String Syntax1":"arealUnit unitOfMeasure\nunitOfMeasure keywords: ACRES | ARES | HECTARES | SQUARECENTIMETERS |
SQUAREDECIMETERS | SQUAREINCHES | SQUAREFEET | SQUAREKILOMETERS |
SQUAREMETERS | SQUAREMILES | SQUAREMILLIMETERS | SQUAREYARDS | SQUAREMAPUNITS
|UNKNOWN","Scripting Object3":". _ .","ArcObjects":"GPArealUnit"},
{"Data Type":"Boolean","Description":"A boolean value.","String Syntax1":"TRUE | FALSE","Scripting Object3":". _ .","ArcObjects":"GPBoolean"},
{"Data Type":"CAD Drawing Dataset","Description":"A vector data source with a mix of feature types with\nsymbology. The dataset is not usable for feature class-
based queries or analysis.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DECadDrawingDataset"},
{"Data Type":"Catalog Root","Description":"The top-level node in the catalog tree.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DECatalogRoot"},
{"Data Type":"Cell Size","Description":"The cell size used by Spatial Analyst.","String Syntax1":"MAXOF | MINOF | value","Scripting Object3":". _ .","ArcObjects":"GPSACellSize"},
{"Data Type":"Composite Datatype","Description":"A collection of datatypes.","String Syntax1":"... dependent on datatypes in collection...","Scripting Object3":". _ .","ArcObjects":"GPCompositeDataType  [abstract\ndatatype]"},
{"Data Type":"Composite Layer","Description":"A reference to a several children layers, including\nsymbology and rendering properties.","String Syntax1":"layerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPCompositeLayer\nDECompositeLayer"},
{"Data Type":"Compression","Description":"Specifies the type of compression used for a raster.","String Syntax1":"LZ77 |\nJPEG |
JPEG2000 |
NONE","Scripting Object3":". _ .","ArcObjects":"GPRasterGDBEnvCompression"},
{"Data Type":"Coordinate System","Description":"A reference framework—such as the UTM\nsystem—consisting of a set of points, lines, and/or
surfaces, and a set of rules, used to define the positions of
points in two and three dimensional space.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"GPCooridnateSystem"},
{"Data Type":"Coordinate Systems Folder","Description":"A folder on disk storing coordinate systems.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DESpatialReferencesFolder"},
{"Data Type":"Coverage","Description":"A courage dataset, a proprietary data model for storing\ngeographic features as points, arcs, polygons with
associated feature attribute tables.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DECoverage"},
{"Data Type":"Coverage Feature Class","Description":"A coverage feature classes such as point, arc, node,\nroute, route system, section, polygon, and region.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DECoverageFeatureClass\nICoverageFeatureClass
ICoverageFeatureClass2"},
{"Data Type":"Database Connections","Description":"The database connection folder in ArcCatalog.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEDiskConnection"},
{"Data Type":"Dataset","Description":"A collection of related data, usually grouped or stored\ntogether.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEDatasetType [abstract datatype ]"},
{"Data Type":"Date","Description":"A date value.","String Syntax1":"format depends on the regional settings of the computer;","Scripting Object3":". _ .","ArcObjects":"GPDate"},
{"Data Type":"dBASE Table","Description":"Attribute data stored in dBASE format.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEDbaseTable\nITable"},
{"Data Type":"Decimate","Description":"Specifies a subset of nodes of a TIN to create a\ngeneralized version of that TIN.","String Syntax1":"ZTOLERANCE Z_Tolerance maxNumberOfNodes |\nCOUNT maxNumberOfNodes","Scripting Object3":". _ .","ArcObjects":"DecimateNodes\nDecimateNodesByCount"},
{"Data Type":"Disk Connection","Description":"An access path to a data storage device.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEDiskConnection"},
{"Data Type":"Double","Description":"Any floating point number will be stored as a double-\nprecision 64-bit value.","String Syntax1":"example: 5.6","Scripting Object3":". _ .","ArcObjects":"GPDouble"},
{"Data Type":"Envelope","Description":"The coordinate pairs that define the minimum bounding\nrectangle the data source fall within.","String Syntax1":"X_Minimum Y_Minimum X_Maximum Y_Maximum","Scripting Object3":". _ .","ArcObjects":"GPEnvelope"},
{"Data Type":"Evaluation Scale","Description":"The scale value range and increment value applied to\ninputs in a weighted overlay operation.","String Syntax1":"EvaluationScale Minimum Maximum Increment\nEvaluationScale: '1 to 9 by 1' | '1 to 5 by 1' | '1 to 3 by 1' | '-1 to 1 by 1' |
'-5 to 5 by 1' | '-10 to 10 by 2'","Scripting Object3":". _ .","ArcObjects":"GPEvaluationScale"},
{"Data Type":"Extent","Description":"Specifies the coordinate pairs that define the minimum\nbounding rectangle (xmin, ymin and xmax, ymax) of a
data source. All coordinates for the data source fall within
this boundary.","String Syntax1":"catalogPath | X_Minimum Y_Minimum X_Maximum Y_Maximum","Scripting Object3":". _ .","ArcObjects":"GPExtent"},
{"Data Type":"Feature Class","Description":"A collection of spatial data with the same shape type:\npoint, multipoint, polyline, polygon.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEFeatureClass\nIFeatureClass
ICoverageFeatureClass"},
{"Data Type":"Feature Dataset","Description":"A collection of feature classes that share a common\ngeographic area and the same spatial reference system.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEFeatureDataset\nIFeatureDataset"},
{"Data Type":"Feature Layer","Description":"A reference to a feature class, including symbology and\nrendering properties. [.lyr]","String Syntax1":"featurelLayerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPFeatureLayer\nIFeatureLayer"},
{"Data Type":"Field","Description":"A column in a table that stores the values for a single\nattribute","String Syntax1":"fieldName","Scripting Object3":"Field","ArcObjects":"Field\nIField"},
{"Data Type":"Field Info","Description":"The details about a field in a FieldMap.","String Syntax1":""fldName newFldName visible;fldName1 newFldName1 visible1;...;fldNameN\nnewFldNameN visibleN"","Scripting Object3":"FieldInfo","ArcObjects":"GPFieldInfo"},
{"Data Type":"Field Mappings","Description":"A collection of fields in one or more input tables.","String Syntax1":"use String Object; use of String Syntax not recommended;\ncatalogPath | SR_ID","Scripting Object3":"FieldMap;\nFieldMappings","ArcObjects":"GPFieldMapping"},
{"Data Type":"File","Description":"A file on disk.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEFile\nIFile"},
{"Data Type":"Folder","Description":"Specifies a location on a disk where data is stored.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEFolder"},
{"Data Type":"Formulated Raster","Description":"A raster surface whose cell values are represented by a\nformula or constant.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"GPRasterFormulated"},
{"Data Type":"GeoDataServer","Description":"A coarse grain object that references a geodatabase.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEGeoDataServer"},
{"Data Type":"Geodataset","Description":"A collection of data with a common theme in a\ngeodatabase.","String Syntax1":"catalogPath;catalogPath1;...;catalogPathN","Scripting Object3":". _ .","ArcObjects":"[abstract datatype ]"},
{"Data Type":"Geometric Network","Description":"A linear network represented by topologically connected\nedge and junction features. Feature connectivity is based
on their geometric coincidence.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEGeometricNetworkType\nDEGeometricNetwork"},
{"Data Type":"Geostatistical Value Table","Description":"A collection of data sources and fields that define a\ngeostatistical layer.","String Syntax1":"catalogPath field;catalogPath1 field1;...;catalogPathN fieldN","Scripting Object3":". _ .","ArcObjects":"GPGAValueTable"},
{"Data Type":"Group Layer","Description":"A collection of layers that appear and act as a single layer.\nGroup layers make it easier to organize a map, assign
advanced drawing order options, and share layers for use
in other maps.","String Syntax1":""groupLayerName;groupLayerName1;...;groupLayerNameN" |\n"catalogPath;catalogPath1;...;catalogPathN"","Scripting Object3":". _ .","ArcObjects":"GPGroupLayer"},
{"Data Type":"Horizontal Factor","Description":"The relationship between the horizontal cost factor and\nthe horizontal relative moving angle.","String Syntax1":"rasterName BINARY ZeroFactor CutAngle |\ncatalogPath BINARY ZeroFactor CutAngle |
rasterName FORWARD ZeroFactor CutAngle SideValue |
catalogPath FORWARD ZeroFactor CutAngle SideValue |
rasterName LINEAR ZeroFactor CutAngle Slope |
catalogPath LINEAR ZeroFactor CutAngle Slope |
rasterName INVERSE LINEAR ZeroFactor CutAngle Slope |
catalogPath INVERSE LINEAR ZeroFactor CutAngle Slope |
rasterName TABLE tableName |
catalogPath TABLE tableName |
rasterName TABLE catalogPath|
catalogPath TABLE catalogPath","Scripting Object3":". _ .","ArcObjects":"GPSAHorizontalFactor"},
{"Data Type":"Index","Description":"A data structure used to speed the search for records in a\ngeographic datasets and database.","String Syntax1":"number","Scripting Object3":". _ .","ArcObjects":"Index"},
{"Data Type":"INFO Expression","Description":"A syntax for defining and manipulating data in an INFO\ntable.","String Syntax1":"SUBSET itemName operator value |\nSUBSET itemName operator value CONNECTOR itemName 1 operator1 value1 CONNECTOR
... CONNECTOR itemNameN operatorN valueN |
ADD itemName operator value |
ADD itemName operator value CONNECTOR itemName 1 operator1 value1 CONNECTOR ...
CONNECTOR itemNameN operatorN valueN |
SWITCH itemName operator value |
SWITCH itemName operator value CONNECTOR itemName 1 operator1 value1 CONNECTOR
... CONNECTOR itemNameN operatorN valueN","Scripting Object3":". _ .","ArcObjects":"GPINFOExpression"},
{"Data Type":"INFO Item","Description":"An item in an INFO table.","String Syntax1":"itemName","Scripting Object3":". _ .","ArcObjects":"GPArcInfoItem"},
{"Data Type":"INFO Table","Description":"A table in an INFO Database.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEArcInfoTable\nIArcInfoTable"},
{"Data Type":"Layer","Description":"A reference to a data source, such as a shapefile,\ncoverage, geodatabase feature class, or raster, including
symbology and rendering properties. [.lyr]","String Syntax1":"layerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"[abstract datatype]"},
{"Data Type":"Layer File","Description":"A file with a .lyr extension that stores the layer defintion,\nincluding symbology and rendering properties.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DELayer\nILayer"},
{"Data Type":"Line","Description":"A shape, straight or curved, defined by a connected series\nof unique x,y coordinate pairs.","String Syntax1":"coordinateList","Scripting Object3":". _ .","ArcObjects":"GPLine"},
{"Data Type":"Linear unit","Description":"A linear unit type and value such as meter or feet.","String Syntax1":"linearUnit unitOfMeasure\nunitOfMeasure keywords: CENTIMETERS | DECIMALDEGREES | DECIMETERS | FEET | INCHES
| KILOMETERS | METERS | MILES | MILLIMETERS | NAUTICALMILES | POINTS |
UNKNOWN | YARDS","Scripting Object3":". _ .","ArcObjects":"GPLinearUnit"},
{"Data Type":"Long","Description":"An integer number value.","String Syntax1":"number","Scripting Object3":". _ .","ArcObjects":"GPLong"},
{"Data Type":"M Domain","Description":"A range of lowest and highest possible value for m\ncoordinates.","String Syntax1":"M_Minimum M_Maximum","Scripting Object3":". _ .","ArcObjects":"GPMDomain"},
{"Data Type":"MultiValue","Description":"A collection of values stored in one column in a value\ntable.","String Syntax1":"string;string1;...;stringN","Scripting Object3":". _ .","ArcObjects":"GPMultiValue"},
{"Data Type":"Neighborhood","Description":"The shape of the area around each cell used to calculate\nstatistics.","String Syntax1":"ANNULUS InnerRadius OuterRadius Units |\nCIRCLE Radius Units |
RECTANGLE Height Width Units |
WEDGE StartAngle EndAngle Radius Units |
IRREGULAR KernelFileName | catalogPath |
WEIGHT KernelFileName or catalogPath
Units keywords: CELL | MAP","Scripting Object3":". _ .","ArcObjects":"GPSANeighborhood"},
{"Data Type":"Network Analyst Class\nFieldMap","Description":"A mapping between location properties in a network\nanalyst layer (such as stops, facilities, and incidents) and
a point feature class.","String Syntax1":"property field defaultValue","Scripting Object3":". _ .","ArcObjects":"NAClassFieldMap"},
{"Data Type":"Network Analyst Hierarchy\nSettings","Description":"A hierarchy attribute that divides hierarchy values of a\nnetwork dataset into three groups using two integers. The
first integer, high_rank_ends, sets the ending value of the
first group; the second number, low_rank_begin, sets the
beginning value of the third group.","String Syntax1":"NONE |\nHIERARCHY defaultRanges |
HIERARCHY customRanges upTo andHigher","Scripting Object3":". _ .","ArcObjects":"GPNAHierarchySettings"},
{"Data Type":"Network Analyst Layer","Description":"A special group layer used to express and solve network\nrouting problems. Each sublayer, held in-memory, in a
Network Analyst layer represent some aspect of the
routing problem and the routing solution.","String Syntax1":"layerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPNALayer\nINALayer"},
{"Data Type":"Network Dataset","Description":"A collection of topologically connected network elements\n(edges, junctions, and turns), derived from network
sources and associated with a collection of network
attributes.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DENetworkDataset\nINetworkDataset"},
{"Data Type":"Network Dataset Layer","Description":"A reference to a network dataset, including symbology\nand rendering properties.","String Syntax1":"layerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPNetworkDatasetLaye"},
{"Data Type":"Point","Description":"A pair of x,y coordinates.","String Syntax1":"coordinatePair","Scripting Object3":"Point","ArcObjects":"GPPoint"},
{"Data Type":"Polygon","Description":"A connected sequence of x,y coordinate pairs, where the\nfirst and last coordinate pair are the same.","String Syntax1":"coordinateList","Scripting Object3":". _ .","ArcObjects":"GPPolygon"},
{"Data Type":"Projection File","Description":"A file storing coordinate system information for spatial\ndata. [.prj]","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEPrjFile\nIFile"},
{"Data Type":"Pyramid","Description":"Specifies if pyramids will be built.","String Syntax1":"NONE |\nPYRAMIDS pyramidLevel sampleMethod
sampleMethod keywords: NEAREST | BILINEAR | CUBIC","Scripting Object3":". _ .","ArcObjects":"GPRasterGDBEnvPyramid"},
{"Data Type":"Radius","Description":"Specifies which surrounding points will be used for\ninterpolation.","String Syntax1":"FIXED Distance Min#OfPts | VARIABLE NumOfPts MaxDistance","Scripting Object3":". _ .","ArcObjects":"GPSARadius"},
{"Data Type":"Random Number Generator","Description":"Specifies the seed and the generator to be used when\ncreating random values.","String Syntax1":"seed randomGenType\nrandomGenType keywords: STANDARD_C | ACM599 | MERSENNE_TWISTER","Scripting Object3":". _ .","ArcObjects":"GPRandomNumberGenerator"},
{"Data Type":"Raster Band","Description":"A layer in a raster dataset.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DERasterBand\nIRasterBand"},
{"Data Type":"Raster Catalog","Description":"A collection of raster datasets defined in a table; each\ntable records defines an individual raster datasets in the
catalog.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DERasterCatalog\nIRasterCatalog"},
{"Data Type":"Raster Catalog Layer","Description":"A reference to a raster catalog, including symbology and\nrendering properties.","String Syntax1":"rasterCatalogLayer | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPRasterCatalogLayer\nIRasterCatalogLayer"},
{"Data Type":"Raster Layer","Description":"A reference to a raster, including symbology and\nrendering properties.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"GPRasterLayer\nIRasterLayer"},
{"Data Type":"Raster Statistics","Description":"Specifies if raster statistics will be built.","String Syntax1":"NONE |\nSTATISTICS X-SkipFactor Y-SkipFactor statsIgnoreValue","Scripting Object3":". _ .","ArcObjects":"GPRasterGDBEnvStatistics"},
{"Data Type":"Relationship Class","Description":"The details about the relationship between objects in the\ngeodatabase.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DERelationshipClass\nIRelationshipClass"},
{"Data Type":"Remap","Description":"A table that defines how raster cell values will be\nreclassified.","String Syntax1":"OldValues NewValue ClassifyMethod\nOldValues: number | range | string | NoData
NewValue: number | range | string | NoData
ClassifyMethod keywords: MANUAL | EQUALINTERVAL | DEFINEDINTERVAL | QUANTILE |
NATURALBREAKS | STANDARDDEVIATION","Scripting Object3":". _ .","ArcObjects":"GPSANumberRemap\nGPSAStringRemap"},
{"Data Type":"Route Measure Event\nProperties","Description":"Specifies the fields on a table that describe events that\nare measured by a linear reference route system.","String Syntax1":"inEventProperties POINT mField |\ninEventProperties LINE fromMField toMField","Scripting Object3":". _ .","ArcObjects":"GPRouteMeasureEventProperties"},
{"Data Type":"SemiVariogram","Description":"Specifies the distance and direction representing two\nlocations that is used to quantify autocorrelation.","String Syntax1":"ORDINARY  SPHERICAL Lag size Major range Partial sill Nugget |\nORDINARY  CIRCULAR Lag size Major range Partial sill Nugget |
ORDINARY  EXPONENTIAL Lag size Major range Partial sill Nugget |
ORDINARY  GAUSSIAN Lag size Major range Partial sill Nugget |
ORDINARY  LINEAR  Lag size Major range Partial sill Nugget |
UNIVERSAL  LINEARDRIFT Lag size Major range Partial sill Nugget |
UNIVERSAL  QUADRATICDRIFT  Lag size Major range Partial sill Nugget","Scripting Object3":". _ .","ArcObjects":"GPSASemiVariogram"},
{"Data Type":"Shapefile","Description":"Spatial data in shapefile format. [.shp]","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEShapefile\nIFeatureclass"},
{"Data Type":"Spatial Reference","Description":"The coordinate system used to store a spatial dataset,\nincluding the spatial domain.","String Syntax1":"use String Object; use of String Syntax not recommended;\ncatalogPath | SR_ID","Scripting Object3":"Spatialreference","ArcObjects":"GPSpatialReference\nISpatialReference"},
{"Data Type":"SQL Expression","Description":"A syntax for defining and manipulating data from a\nrelational database.","String Syntax1":"fieldName operator value","Scripting Object3":". _ .","ArcObjects":"GPSQLExpression"},
{"Data Type":"String","Description":"A text value.","String Syntax1":"any combination of characters including spaces","Scripting Object3":". _ .","ArcObjects":"GPString"},
{"Data Type":"Table","Description":"Tabular data.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DETable"},
{"Data Type":"Table View","Description":"A representation of tabular data for viewing and editing\npurposes, stored in memory or on disk.","String Syntax1":"tableViewName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPTableView\nIFeatureclass
ITable
ILayer"},
{"Data Type":"Terrain","Description":"A multiresolution TIN.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DETerrain"},
{"Data Type":"Terrain Layer","Description":"A reference to a terrain, including symbology and\nrendering properties. It’s used to draw a terrain.","String Syntax1":"terrainLayerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPTerrainLayer"},
{"Data Type":"Text File","Description":"Data stored in ASCII format.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DETextFile"},
{"Data Type":"Tile Size","Description":"Specifies the width and the height of a data stored in\nblock.","String Syntax1":"width height","Scripting Object3":". _ .","ArcObjects":"GPRasterGDBEnvTileSize"},
{"Data Type":"Time configuration","Description":"Specifies the time periods used for calculating solar\nradiation at specific locations.","String Syntax1":"SPECIAL DAYS |\nWITHIN A DAY numOfDays startTime endTime |
MULTIPLE DAYS IN A YEAR  year startDay endDay |
WHOLE YEAR WITH MONTHLY INTERVAL year","Scripting Object3":". _ .","ArcObjects":"GPSATimeConfiguration"},
{"Data Type":"TIN  [Triangulated Irregular\nNetwork]","Description":"A vector data structure that partitions geographic space\ninto contiguous, non-overlapping triangles. The vertices of
each triangle are sample data points with x-, y-, and z-
values.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DETin\nITin"},
{"Data Type":"Topo Features","Description":"Features that are  input to the interpolation.","String Syntax1":"catalogPath featureLayer field Type\nType keywords: POINTELEVATION | CONTOUR | STREAM | SINK | BOUNDARY | LAKE","Scripting Object3":". _ .","ArcObjects":"GPSATopoFeatures"},
{"Data Type":"Topology","Description":"A topology that defines and enforces data integrity rules\nfor spatial data.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DETopology\nITopology"},
{"Data Type":"Topology Layer","Description":"A reference to a topology, including symbology and\nrendering properties.","String Syntax1":"topologyLayerName | catalogPath","Scripting Object3":". _ .","ArcObjects":"GPTopologyLayer\nITopologyLayer"},
{"Data Type":"Variant","Description":"A data value that can contain any basic type: boolean,\ndate, double, long, and string.","String Syntax1":"any combination of characters including spaces","Scripting Object3":". _ .","ArcObjects":"GPVariant"},
{"Data Type":"ValueTable","Description":"A collection of columns of values.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"GPValueTable"},
{"Data Type":"Vertical Factor","Description":"Specifies the relationship between the vertical cost factor\nand the vertical relative moving angle.","String Syntax1":"BINARY ZeroFactor LowCutAngle HighCutAngle |\nLINEAR ZeroFactor LowCutAngle HighCutAngle Slope |
INVERSE LINEAR ZeroFactor LowCutAngle HighCutAngle Slope |
SYMMETRIC LINEAR ZeroFactor LowCutAngle HighCutAngle Slope |
SYMMETRIC INVERSE LINEAR  ZeroFactor LowCutAngle HighCutAngle Slope |
COS LowCutAngle HighCutAngle Power |
SEC  LowCutAngle HighCutAngle Power |
COS_SEC LowCutAngle HighCutAngle COS_Power SEC_Power |
SEC_COS  LowCutAngle HighCutAngle COS_Power SEC_Power |
TABLE tableName |
TABLE catalogPath","Scripting Object3":". _ .","ArcObjects":"GPSAVerticalFactor"},
{"Data Type":"VPF Coverage","Description":"Spatial data stored in Vector Product Format.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEVPFCoverage"},
{"Data Type":"VPF Table","Description":"Attribute data stored in Vector Product Format.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEVPFTable"},
{"Data Type":"Weighted Overlay Table","Description":"A table with data to combine multiple rasters by applying a\ncommon measurement scale of values to each raster,
weighting each according to its importance.","String Syntax1":""rasterName %Influence Field Remap2";"..." |\n"catalogPath %Influence Field Remap2";"...";","Scripting Object3":". _ .","ArcObjects":"GPSAWeightedOverlayTable"},
{"Data Type":"Weighted Sum","Description":"Specifies data for overlaying several rasters multiplied\neach by their given weight and then summed.","String Syntax1":""rasterName Field Weight";"rasterName1 Field1 Weight1";" ..."; |\n"catalogPath Field Weight";"catalogPath1 Field1 Weight1";" ...";","Scripting Object3":". _ .","ArcObjects":"GPWeightedSum"},
{"Data Type":"Workspace","Description":"A container such as a geodatabase or folder.","String Syntax1":"catalogPath","Scripting Object3":". _ .","ArcObjects":"DEWorkspace"},
{"Data Type":"XY Domain","Description":"A range of lowest and highest possible values for x,y\ncoordinates.","String Syntax1":"X_Minimum  Y_Minimum  X_Maximum  Y_Maximum","Scripting Object3":". _ .","ArcObjects":"GPXYDomain"}];