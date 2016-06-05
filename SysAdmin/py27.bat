@echo off
if not defined PYTHONHOME call :set_env %~n0
python %*
goto :eof

:set_env
  :: extract python version from last 2 characters of batch filename
  set _ver=%1
  set _ver=%_ver:~-2%
  
  set PYTHONHOME=C:\Python%_ver%\ArcGIS10.3
  set PROMPT=[py%_ver%] $p$_$g 
  
  set _path=%PYTHONHOME%
  call addpath _path
  set _path=%PYTHONHOME%\Scripts
  call addpath _path

  set python

  set _path=
  set _ver=
  goto :eof
