@echo off
if not defined PYTHONHOME call :set_env %~n0
python %_opts% %*
goto :eof

:set_env
  set _ver=34_x64
  set PYTHONHOME=C:\Python34_x64
  set PROMPT=[py%_ver%] $p$_$g 
  
  set _path=C:\Python%_ver%
  call addpath _path
  set _path=C:\Python%_ver%\Scripts
  call addpath _path
  
  :: enables if py env was not set on invocation,
  :: echo version number and exit.
  set _opts=--version

  set python

  set _path=
  set _ver=
  goto :eof
