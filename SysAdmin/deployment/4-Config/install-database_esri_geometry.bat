@setlocal
@set _ver=%1
@echo.  ----------------------------------------------------------------------------------
@echo.  Installing database files for using Esri Geometry in SQLite, Postgres, and Oracle
@echo.
@xcopy /v /y %~dp0\database_esri_geometry\%_ver%\x86 C:\ArcGIS\Pro\bin\x86
@xcopy /v /y %~dp0\database_esri_geometry\%_ver%\x64 C:\ArcGIS\Pro\bin\x64
@echo.  ----------------------------------------------------------------------------------
@REM start C:\ArcGIS\Pro\bin\
