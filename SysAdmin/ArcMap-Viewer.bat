set _fname=%~n0
set _level=%_fname:*-=%
set ESRI_SOFTWARE_CLASS=%_level%
start /b c:\ArcGIS\Desktop10.2\bin\ArcMap.exe