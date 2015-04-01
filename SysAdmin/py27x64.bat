@echo off
if not defined PYTHONHOME call :set_env %~n0
python %_opts% %*
goto :eof

:set_env
  set PYTHONHOME=C:\Python27\ArcGISx6410.3
  set PROMPT=[2.7_x64] $p$_$g 
  
  set _path=%PYTHONHOME%
  call addpath _path
  set _path=%PYTHONHOME%\Scripts
  call addpath _path
  
  :: enables if py env was not set on invocation,
  :: echo version number and exit.
  set _opts=--version

  set python

  set _path=
  set _ver=
  goto :eof
