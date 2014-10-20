@echo off
:: Homepage:  https://github.com/maphew/arcplus/blob/master/SysAdmin/uninstall-ALL-ArcGIS-products.md
:: Copyright 2013 Environment Yukon, License: MIT/X (open source)
:: Author:  Matt.Wilkie@gov.yk.ca
::
set _product_codes=%1
:: Comment out this next line to enable passing product codes on command line
:: Note: lack of quotes after "set ..." is deliberate
if exist "%~dp0\product-codes.txt" set _product_codes=%~dp0\product-codes.txt

echo. ---------------------------------------------------------------------------
echo.           Uninstall all ArcGIS products
echo. ---------------------------------------------------------------------------
if not exist "%_product_codes%" goto :no_codes_file

:: msiexec optional parameters here
:: remove '/passive' to hide the pop-up progress window and run silently
set _opt=/passive 
if "%2"=="/silent" set _opt=

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

:from_file
  :: Parse product name and id code from Product-Codes.txt
  :: http://ss64.com/nt/for_f.html
  echo.
  echo.           using "%_product_codes%" for Product ID list
 
  for /f "tokens=1,2 delims=^{" %%a in (%1) do (^
    if "%%b"=="" (echo ----- %%a -----) else (echo {%%b - %%a)
    call :uninstall {%%b
    )
  goto :eof

:no_codes_file
  echo.
  echo. Product code file "%_product_codes%" not found
  echo.
  call :Usage
  echo.&& pause
  goto :eof

:Usage  
  echo. Usage:  
  echo.       %~n0 product-codes.txt
  echo.       %~n0 product-codes.txt /silent
  echo.
  goto :eof
