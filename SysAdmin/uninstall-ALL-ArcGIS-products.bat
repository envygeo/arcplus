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
