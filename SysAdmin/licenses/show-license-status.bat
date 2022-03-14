@echo off
:: Report  ESRI License Manager  status
:: 2009.August.05 *  matt.wilikie@gov.yk.ca * this script is public domain.
:: Requires Lmutil.exe and Lmgrd.exe in PATH.  Find them under license 
:: manager in C:\Program Files. They can be copied and run from anywhere.
setlocal
path=%path%;%~dp0\bin

:: use hardcoded server unless  server/ip specified on command line
if [%1]==[] (
      set arclic_server=ENVGEOSERVER
   ) else (
      set arclic_server=%1
      )

lmutil lmstat -a -c @%arclic_server%

pause
