@echo off
:: Homepage: https://github.com/envygeo/arcplus/tree/master/SysAdmin/deployment
:: Copyright 2013-2017 Environment Yukon, License: MIT/X (open source)
:: Author:  Matt.Wilkie@gov.yk.ca
::
setlocal
set _product_codes=%1
if not defined _product_codes call :default_codes_choice

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
  if exist %SystemRoot%\Installer\%1 (^
    echo Found: %SystemRoot%\Installer\%1
    %SystemRoot%\System32\msiexec.exe /x %1 /qn /norestart /l*+ %temp%\%~n0-%COMPUTERNAME%.log %_opt%
    )
  goto :eof

:from_file
  :: Parse product name and id code from Product-Codes.txt
  :: http://ss64.com/nt/for_f.html
  :: Ignores anything preceeding left-side curly brace: `{`
  :: Anything following closing `}` will be passed to msiexec
  :: and likely cause error.
  ::
  ::      left of `{` becomes %%a
  ::      right of `{` becomes %%b
  echo.
  echo.           using "%1" for Product ID list
 
  for /f "tokens=1,2 delims=^{" %%a in (%1) do (^
    if "%%b"=="" (echo ----- %%a -----) else (echo {%%b - %%a)
    call :uninstall {%%b
    )
  goto :eof

:default_codes_choice
  echo.
  echo. No code file provided.
  echo.
  call :usage
  echo.
  choice /c YN /d N /t 15 /n /m "Use default 'product-codes\main.txt'? (Defaults to No in 15s) [y,N] "
  echo.
  echo %errorlevel%
  if errorlevel 2 goto :eof
  
  :: Note: lack of quotes after "set ..." is deliberate
  if exist "%~dp0\product-codes\main.txt" set _product_codes=%~dp0\product-codes\main.txt
  
  goto :eof
  
:no_codes_file
  echo.
  echo. Product code file "%_product_codes%" not found
  echo.
  call :usage
  echo.&& pause
  goto :eof

:usage  
  echo. Usage:  
  echo.       %~n0 product-codes.txt
  echo.       %~n0 product-codes.txt /silent
  echo.
  goto :eof
