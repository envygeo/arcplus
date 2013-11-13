@echo off
set _product_codes=%1
echo. ---------------------------------------------------------------------------
echo.
echo.           Uninstall all ArcGIS products
echo.
echo.           using "%_product_codes%" for Product ID list
echo. ---------------------------------------------------------------------------
echo.
if not exist "%1" goto :no_codes_file
set /p _verify="Are you sure you want to continue? [y/N] " || set _verify=N
if /i not "%_verify%"=="Y" goto :eof

:: msiexec optional parameters here
:: remove '/passive' to hide the pop-up progress window and run silently
set _opt=/passive 
if "%2"=="silent" set _opt=

call :from_file %_product_codes%

echo.
echo. Finished, log at:
echo.
echo. %temp%\%~n0-%COMPUTERNAME%.log
echo.
echo. ---------------------------------------------------------------------------
ping -n 7 localhost> nul
goto :eof

:: ---------------------------------------------------------------------------
:uninstall
  :: %1 = product code
  %SystemRoot%\System32\msiexec.exe /x %1 /qn /norestart /l*+ %temp%\%~n0-%COMPUTERNAME%.log %_opt%
  goto :eof


:: ---------------------------------------------------------------------------
:: Product codes are from 
::  http://support.esri.com/en/knowledgebase/techarticles/detail/28709
::
:: The list above is not complete, it's missing ArcPad and maybe others.
:: Product Codes for most Esri setups can be found in the setup.ini file delivered with 
:: the other installation files.
::
:: Syntax of "product-codes.txt":
::
::    Product Name {a1a1a1a-a1a1a-a1a1a...}
::
::    ArcGIS 8.2
::    ArcGIS Desktop {A149DEA2-1D5B-11D5-9F76-00C04F6BC7A1}
::    ArcGIS ArcObjects Developer Kit {52069752-B5E9-11D5-8110-00C04FA070E5}
::    ArcGIS Tutorial Data {440A069B-9016-11D4-80CB-00C04FA070E5}
::    ...etc.
::
:: -----
:: An alternate approach is to retrieve dynamically with (be patient, takes a long time):
::
::  wmic product where "Name like '%ArcGIS%'" ^
::    get Name, IdentifyingNumber, Version 
::

:from_file
  :: Parse product name and id code from Product-Codes.txt
  :: http://ss64.com/nt/for_f.html
  echo.
  for /f "tokens=1,2 delims=^{" %%a in (%1) do (^
    if "%%b"=="" (echo ----- %%a -----) else (echo {%%b - %%a)
    call :uninstall {%%b
    )
  goto :eof

:no_codes_file
  echo.
  echo. "%1" not found
  echo.
  call :Usage
  goto :eof

:Usage  
  echo. Usage:  
  echo.       %~n0 product-codes.txt
  echo.       %~n0 product-codes.txt /silent
  echo.
  goto :eof
