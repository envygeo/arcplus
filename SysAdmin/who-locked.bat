@echo off
:: Who has created the .lock files?
setlocal EnableDelayedExpansion
if not exist "%1" goto :Usage

call :find_locks %*
if defined _locks call :machine_from_lock !_locks!
if defined _machines (
  echo Machine list: !_machines!
  call :uniq !_machines!
  echo No dupes: !_result!
  )

goto :eof

for %%a in (%1) do (
  pushd %%a
    :: parse "ENV-Y226526" from "Default.ENV-Y226526.3432.4836.sr.lock"
    for /f "tokens=3 delims=^." %%b in ('dir /s/b *.lock') do (
      call :get_user %%b
      )
  popd
  )
goto :eof  
  
:find_locks
  echo. &echo --- Searching "%1" for .lock files --- &echo.
  pushd %1
  for /f "usebackq" %%a in (`dir /s/b *.lock 2^>nul`) do (
    echo "%%a"
    set _locks="%%a" !_locks!
    )
  REM if defined _locks echo Lock list: !_locks!
  popd
  :: Remove `2^>nul` to stop swallowing errors from `dir`
  :: (is used to hide "file not found")
  goto :eof

:machine_from_lock
  echo. &echo --- Extracting machine names --- &echo.
  :: %* is list of lock files
  :: "z:\V5\ENV_all_scales.gdb\_gdb.ENV-Y226526.3848.8100.sr.lock
  :: We expect name to be between 2nd and 3rd dot: "ENV-Y226526"
  for %%a in (%*) do (
    for /f "tokens=3 delims=." %%b in (%%a) do (
      set _machines=!_machines! %%b
      ))
  goto :eof

:uniq
  :: strip duplicates
  set _line=
  for %%a in (%*) do (
    set _line=%%a
    if not "%%a"=="!_line!" set _result=!_result!
    )
  echo ...line: !_line!
  echo ...result: !_result!
  goto :eof
  
  
:get_user
  echo --- get_user %*
  wmic /node:"%1" computersystem get username
  goto :eof

:Usage
  echo.
  echo. Who created the .lock file?
  echo.
  echo.   %~n0 [path\to\file.gdb]
  echo.
  goto :eof


REM http://mysites.yukonnect.gov.yk.ca/users/mhwilkie/env-gis-unit/_layouts/OneNote.aspx?id=%2fusers%2fmhwilkie%2fenv-gis-unit%2fSiteAssets%2fENV%20GIS%20Unit%20notebook&wd=target%28Tips%20and%20Tricks.one%7cEA18D0B9-F53F-4841-AED2-E7F34907E59E%2fWho%20is%20logged%20on%20to%20computer%3f%7c9B11DD54-2E4B-4AA7-A9B0-D51600B490F4%2f%29
REM onenote:http://mysites.yukonnect.gov.yk.ca/users/mhwilkie/env-gis-unit/SiteAssets/ENV%20GIS%20Unit%20notebook/Tips%20and%20Tricks.one#Who%20is%20logged%20on%20to%20computer&section-id={EA18D0B9-F53F-4841-AED2-E7F34907E59E}&page-id={9B11DD54-2E4B-4AA7-A9B0-D51600B490F4}&end  