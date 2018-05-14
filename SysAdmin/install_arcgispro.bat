REM Upstream source: https://community.esri.com/docs/DOC-8930-arcgis-pro-silent-install-script
REM Selectively applied (see details in git history)
:: install_arcgispro.bat
:: Silent install of ArcGIS Pro 
:: 
:: INSTRUCTIONS:
:: 1) Edit this script as instructed below in the comments
:: 2) Save with ".bat" extension
:: 3) Open an administrative command window.
:: 4) Run this install script from the command line
::    Alternatively, deployment software can be used to run the script.
::
:: Required files, this script assumes the script is in the same
:: folder as the "Esri" folder below:
:: 
:: install_arcgispro.bat
:: \---Esri
::     +--ArcGISPro
::          ArcGISPro.cab
::          ArcGISPro.msi
::          *.msp files (if any - for example 1.4.1 patch to 1.4)
::     +--ArcGISProHelp
::          ArcGISProHelp.cab
::          ArcGISProHelp.msi      
::
::
:: Author: Curtis Price, cprice@usgs.gov
::
:: History:
:: 01/30/2015 ArcGIS Pro 1.0 - Initial release
:: 08/19/2015 Added .NET 4.5 check
:: 11/02/2016 Update for Pro 1.3 / 1.3.1
:: 06/07/2017 Setup to apply any .msp files in Pro .msi folder
:: 03/18/2018 Added CHECKFORUPDATESATSTARTUP to install command
::----------------------------------------------------------------
:: This software is provisional and subject to revision; it has
:: not been thoroughly reviewed or received USGS final approval.
:: Users are cautioned to consider carefully the provisional
:: nature of the code before using it for decisions that concern
:: personal or public safety or the conduct of business that
:: involves substantial monetary or operational consequences.
@echo off

:: keep variables local to this script
setlocal

:: %~d0%~p0 is folder where this script resides
set SRC=%~d0%~p0
set LOGDIR=%TEMP%
set INSTALLDIR=C:\ArcGIS\Pro
:: set to 1 to suppress Pro prompting software updates 
:: (useful for managed deployments)
set CHECKUPDATES=0

:: ====================================================================
::                PLEASE DO NOT EDIT BELOW THIS LINE
:: ====================================================================

:: Check for .NET 4.6.1 x64
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

echo.
net session >nul 2>&1
if %errorLevel% == 0 (
  echo Administrative permissions confirmed.
) else (
  echo Current permissions inadequate
  echo ArcGIS Pro install failed
  goto :eof
)


:: Set log file path, prefix at install script runtime
:: Example LOG_PATH result: "%LOGDIR%\ArcGISPro_20120925_1623"
:: (%LOGDIR% is set above)

set DATESTAMP=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
set TIMESTAMP=%TIME:~,2%%TIME:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set LOG_PATH=%LOGDIR%\ArcGISPro_%DATESTAMP%_%TIMESTAMP%
set SILENT=/qb- /passive /norestart

:: Installation starts here

@echo on

:: Install ArcGIS Pro for all users of this computer
msiexec /i "%SRC%\Esri\ArcGISPro\ArcGISPro.msi" ^
 ALLUSERS=1 INSTALLDIR="%INSTALLDIR%" ^
 CHECKFORUPDATESATSTARTUP=%CHECKUPDATES% ^
 /l+ie "%LOG_PATH%_Pro.txt" /l+ie "%LOG_PATH%.txt"  %SILENT%

:: patch updates (.msp files (if any) should be placed in folder with ArcGIS Pro msi
pushd "%SRC%\Esri\ArcGISPro"
for %%p in (*.msp) do %MSIEXEC% /p %%p REINSTALLMODE=omus %SL% 
popd

:: ArcGIS Pro Help (optional) (Delete or comment out to only use web help)
msiexec /i "%SRC%\Esri\ArcGISProHelp\ArcGISProHelp.msi" ^
  /l+ie "%LOG_PATH%_Help.txt" %SILENT%
  

:: Optional: Set registry key to block ArcGIS Pro update prompts
REM %WINDIR%\system32\reg.exe add HKLM\SOFTWARE\ESRI\ArcGISPro\Settings ^
REM   /v CheckForUpdatesAtStartup /t REG_DWORD /d 0 /f
:: TODO: use this as template for fixing bug with mismatch between 
:: mapped drives and UNC paths in Control Panel uninstall source
