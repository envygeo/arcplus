@echo off
:: Batch file to restart ESRI License Manager, can be run as a scheduled task
:: 2008.March.10 *  matt.wilikie@gov.yk.ca * this script is public domain.

:: change this to the ip address or netbios name of your license server
set arclic_server=spellingbee

:: redirect stderr nul to hide error messages which are always present,
:: even on successful shutdown. Hopefully this doesn't hide a real problem.
net stop "arcgis license manager"  2> nul
net start "arcgis license manager"

:: doublecheck that license manager is running and show avaialable licenses
:: but wait for license manager to catch a breath first
ping -n 3 localhost > nul
lmutil lmstat -a -c @%arclic_server%

echo ...
echo.   Pausing for messages
echo.   window will close in 15 seconds...
echo ...
ping -n 15 localhost > nul
