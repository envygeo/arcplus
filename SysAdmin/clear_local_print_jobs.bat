@echo off
:: adapted from http://serverfault.com/questions/14098/delete-old-windows-print-jobs
:: 2010-Jul-08, matt.wilkie@gov.yk.ca
::
echo Printers - Shutting down the print spooler
net stop "print spooler"
echo Printers - Deleting print queues
del c:\WINDOWS\system32\spool\PRINTERS\*.* /q

net start "print spooler"
echo Printers - Print spooler Started
