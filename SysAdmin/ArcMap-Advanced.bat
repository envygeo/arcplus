@echo off
if not defined AGSDESKTOPJAVA goto :NoEnv
set _exe="%AGSDESKTOPJAVA%\bin\ArcMap.exe"
if not exist %_exe% goto :NoExe

call :GetLicense
call :Main
goto :eof

:: ----------------------------------------------
:GetLicense
    :: Determine License level from filename suffix
    :: ArcMap-Editor.bat --> "Editor" license
    set _fname=%~n0
    set _level=%_fname:*-=%
    set ESRI_SOFTWARE_CLASS=%_level%
    goto :eof
    
:Main
    start "Starting ArcMap %_level%" /b %_exe%
    goto :eof

:NoEnv
    echo.
    echo.   AGSDESKTOPJAVA is not defined.
    echo.   I can't determine where ArcGIS is installed.
    echo.
    pause
    goto :eof

:NoExe
    echo.
    echo.   *** Error: %_exe% not found.
    echo.
    pause
    goto :eof
    