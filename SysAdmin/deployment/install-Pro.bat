@echo off
cls
echo.
echo.   Installing ArcGIS Pro without prompts, according to ENV Yukon standards
echo.
setlocal
set root=%~dp0
pushd %~dp0

:: One of: SINGLE_USE, CONCURRENT_USE, NAMED_USER
set AUTHORIZATION_TYPE=NAMED_USER
  :: if NAMED_USER set to licensing portal or arcgis.com url
  set LICENSE_URL=https://maps.example.ca/portal

:: License server(s) hostname or IP address, semicolon delimited.
:: Ignored unless CONCURRENT_USE for auth type
set LICSERVER=@LICSERVER;@BACKUPSERVER

:: One of: VIEWER, EDITOR, PROFESSIONAL
set SOFTWARE_CLASS=Viewer

:: set PORTAL_LIST="<portalURL1>;<portalURL2>". Use semicolons to separate URLs.
set PORTAL_LIST="https://maps.example.ca/portal;https://orgname.maps.argis.com"


:: ----- End of most changed settings -----


:checkPrivileges
  :: courtesy of https://ss64.com/nt/syntax-elevate.html
  echo. & echo Testing: for admin privileges...
  fsutil dirty query %SYSTEMDRIVE% >nul
  if %errorLevel% NEQ 0 (
     echo. ** Please rerun this script from an elevated command prompt. Exiting...
     timeout /t 7
     exit /B 1
  ) 
  echo Success: this script is running elevated.

:checkDotNet
  :: Check for .NET courtesy of @curtvprice
  echo. & echo Testing: for correct Dot Net framework
  REM set key=HKLM\SOFTWARE\Microsoft\.NETFrameworkDOESNOTEXIST
  set key=HKLM\SOFTWARE\Microsoft\.NETFramework
  :: 4.6.1 x64
  %WINDIR%\system32\reg.exe query %key%  /f ".NETFramework,Version=v4.6.1" /k /s >NUL
  if %errorLevel% NEQ 0 (
     echo. ** Microsoft .NET Framework 4.6.1 ^(x64^) must be installed first
     echo.  Run "%root%\4-Config\install-DotNet.vbs"
     echo.  and then try again.
     timeout /t 7
     exit /B 1
  ) 
  echo Success: Microsoft .NET Framework 4.6.1 ^(x64^) verified

  call :install_pro
  call :install_patches

timeout /t 15
popd
goto :eof

:: --------------- Routines ------------------
  
:install_pro
REM https://pro.arcgis.com/en/pro-app/get-started/arcgis-pro-installation-administration.htm
  echo. & echo -- Installing ArcGIS Pro...
  pushd %~dp0\1-Pro
  %SystemRoot%\System32\msiexec.exe /I ^
      %cd%\ArcGISPro.msi ^
      ACCEPTEULA=YES ^
      ALLUSERS=1 ^
      AUTHORIZATION_TYPE=%AUTHORIZATION_TYPE% ^
      CHECKFORUPDATESATSTARTUP=0 ^
      ENABLEEUEI=0 ^
      ESRI_LICENSE_HOST=%LICSERVER% ^
      INSTALLDIR=C:\ArcGIS ^
      LICENSE_URL=%LICENSE_URL% ^
      LOCK_AUTH_SETTINGS=FALSE ^
      PORTAL_LIST=%PORTAL_LIST% ^
      SOFTWARE_CLASS=%SOFTWARE_CLASS% ^
      /L* "%TEMP%\%~nx0.log" ^
      /qb 
  popd
  echo Logfile: "%TEMP%\%~nx0.log"
  goto :eof

:install_patches
  :: patch updates (.msp files, if any) should be placed in folder with ArcGIS Pro msi
  pushd "%root%\1-Pro"
  for %%p in (*.msp) do (
    echo -- Installing patch %%p...
    %SystemRoot%\System32\msiexec.exe /p ^
    %%p ^
    REINSTALLMODE=omus ^
    /L* "%TEMP%\%~nx0_patches.log" ^
    /qb
    echo Logfile: "%TEMP%\%~nx0_patches.log"
    )
  popd
  goto :eof

:: ----- NOTES -----
:: check* routines must appear in top block and can't be called, else
:: the `exit /b` command will only exit the block and not the parent
:: script.
