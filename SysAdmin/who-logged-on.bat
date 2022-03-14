@echo off
:: Who is logged on to the machine?
if "%1"=="" goto :Usage

:get_user
  echo --- get_user %*
  wmic /node:"%1" computersystem get username
  goto :eof

:Usage
  echo.
  echo. %~0 [machine_name]
  echo.
  goto :eof


REM http://mysites.yukonnect.gov.yk.ca/users/mhwilkie/env-gis-unit/_layouts/OneNote.aspx?id=%2fusers%2fmhwilkie%2fenv-gis-unit%2fSiteAssets%2fENV%20GIS%20Unit%20notebook&wd=target%28Tips%20and%20Tricks.one%7cEA18D0B9-F53F-4841-AED2-E7F34907E59E%2fWho%20is%20logged%20on%20to%20computer%3f%7c9B11DD54-2E4B-4AA7-A9B0-D51600B490F4%2f%29
REM onenote:http://mysites.yukonnect.gov.yk.ca/users/mhwilkie/env-gis-unit/SiteAssets/ENV%20GIS%20Unit%20notebook/Tips%20and%20Tricks.one#Who%20is%20logged%20on%20to%20computer&section-id={EA18D0B9-F53F-4841-AED2-E7F34907E59E}&page-id={9B11DD54-2E4B-4AA7-A9B0-D51600B490F4}&end  