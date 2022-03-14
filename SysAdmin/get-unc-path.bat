@REM Get the full UNC path for the specified mapped drive path
@if [%1]==[] goto :Usage
@setlocal enabledelayedexpansion
@set _NetworkPath=
@pushd %1
@echo.
@for /f "tokens=2" %%i in ('wmic path win32_mappedlogicaldisk get deviceid^, providername ^| findstr /i "%CD:~0,2%"') do @(set _NetworkPath=%%i%CD:~2%)
@echo.%_NetworkPath%
@if not [%2]==[] call :info
@popd
@goto :EOF
:: ---------------------------------------------------------------------
:info
  @rem %CD% is set from %%i through some kind of CMD magic
  @rem The rest is standard VarSubstring
  @echo.
  @echo Drive letter:  %CD:~0,2%
  @echo Trailing path: %CD:~2%
    @rem  Extract '\Tools\admin' from 'Z:\Tools\admin'
  @echo Full UNC path: %_NetworkPath%
  @goto :eof
:Usage
  @echo.
  @echo. Get the full UNC path for the specified mapped drive path
  @echo.
  @echo.  %~n0 [mapped drive path] {show-details}
  @goto :eof
  