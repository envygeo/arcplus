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
  @echo Testing for admin privileges...
  fsutil dirty query %SYSTEMDRIVE% >nul
  If %errorLevel% NEQ 0 (
     Echo Failure, please rerun this script from an elevated command prompt. Exiting...
     Ping 127.0.0.1 3>&1 > nul
     Exit /B 1
  ) 
  @echo Success: this script is running elevated.

call :checkDotNet  
call :install_pro

timeout /t 15
popd
goto :eof

:: --------------- Routines ------------------
  
:install_pro
REM https://pro.arcgis.com/en/pro-app/get-started/arcgis-pro-installation-administration.htm
  echo. Installing ArcGIS Pro...
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

:checkDotNet  
:: Check for .NET
  set x64key=HKLM\SOFTWARE\Microsoft\.NETFramework
  :: 4.6.1 x64
  %WINDIR%\system32\reg.exe query %x64key%  /f ".NETFramework,Version=v4.6.1" /k /s >NUL ^
    || ( echo. & echo ** Microsoft .NET Framework 4.6.1 ^(x64^) not installed! ** & goto dotnet_fail)  
  echo Microsoft .NET Framework 4.6.1 ^(x64^) verified
  goto dotnet_ok

:dotnet_fail
  echo ** .NET Check Failed -- Cannot Install ArcGIS Pro **
  goto :eof
:dotnet_ok
  echo ** .NET Check Passed **
  goto :eof