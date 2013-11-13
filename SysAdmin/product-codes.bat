@echo off
:: [28709 - Silently uninstall ArcGIS products](http://support.esri.com/en/knowledgebase/techarticles/detail/28709)
::
:: The list above is not complete, it's missing ArcPad and maybe others.
:: Product Codes for most Esri setups can be found in the setup.ini file delivered with the other installation files.
::
:: Syntax of "product-codes.txt", any line without a left curly brace "{" is ignored
::
::  Product Name {a1a1a1a-a1a1a-a1a1a...}
::
::  ArcGIS 8.2
::  ArcGIS Desktop {A149DEA2-1D5B-11D5-9F76-00C04F6BC7A1}
::  ArcGIS ArcObjects Developer Kit {52069752-B5E9-11D5-8110-00C04FA070E5}
::  ArcGIS Tutorial Data {440A069B-9016-11D4-80CB-00C04FA070E5}
::  ...etc.

call :read_file
goto :eof

:read_file
  :: Parse product name and id code from Product-Codes.txt
  :: http://ss64.com/nt/for_f.html
  for /f "tokens=1,2 delims=^{" %%a in (product-codes.txt) do (^
    echo Product: %%a
    echo code:  {%%b
    )
  goto :eof


:get_id
  :: Parse product id code from name and code string
  :: by deleting the character string '{' and everything before it
  :: http://ss64.com/nt/syntax-replace.html
  ::
  ::  `set _test=ArcGIS Desktop {A149DEA2-1D5B-11D5-9F76-00C04F6BC7A1}`
  ::
  ::  should result in:
  ::      {A149DEA2-1D5B-11D5-9F76-00C04F6BC7A1}
  ::
  set _test=%1
  set _result={%_test:*{=%
  echo. %_test%
  echo. %_result%
  goto :eof

