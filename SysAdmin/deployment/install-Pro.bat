@echo off
cls
echo.
echo.   Installing ArcGIS Pro without prompts, according to ENV Yukon standards
echo.
setlocal
set root=%~dp0
pushd %~dp0

:checkPrivileges
  :: courtesy of https://ss64.com/nt/syntax-elevate.html
  echo. & echo Testing: for admin privileges...
  fsutil dirty query %SYSTEMDRIVE% >nul
  if %errorLevel% NEQ 0 (
     echo ** Please rerun this script from an elevated command prompt. Exiting...
     ping 127.0.0.1 3>&1 > nul
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
     echo ** Microsoft .NET Framework 4.6.1 ^(x64^) must be installed first
     echo.  Run "%root%\4-Config\install-DotNet.vbs"
     echo.  and then try again.
     ping 127.0.0.1 3>&1 > nul
     exit /B 1
  ) 
  echo Success: Microsoft .NET Framework 4.6.1 ^(x64^) verified

  call :install_pro

timeout /t 15
popd
goto :eof

:: --------------- Routines ------------------
  
:install_pro
REM https://pro.arcgis.com/en/pro-app/get-started/arcgis-pro-installation-administration.htm
  echo & . echo. Installing ArcGIS Pro...
  pushd %~dp0\1-Pro
  echo %cd%
  %SystemRoot%\System32\msiexec.exe /I ^
      %cd%\ArcGISPro.msi ^
      ESRI_LICENSE_HOST=LICSERVER ^
      SOFTWARE_CLASS=Viewer ^
      AUTHORIZATION_TYPE=CONCURRENT_USE ^
      LOCK_AUTH_SETTINGS=FALSE ^
      INSTALLDIR=C:\ArcGIS ^
      ALLUSERS=1 ^
      CHECKFORUPDATESATSTARTUP=0 ^
      ENABLEEUEI=0 ^
      /L* "%TEMP%\%~nx0.log" ^
      /qb 
  popd
  echo. Logfile: "%TEMP%\%~nx0.log"
  goto :eof

:: ----- NOTES -----
:: check* routines must appear in top block and can't be called, else
:: the `exit /b` command will only exit the block and not the parent
:: script.
