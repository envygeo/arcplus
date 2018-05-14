REM Install .NET Framework
REM https://support.microsoft.com/en-ca/help/3102436/the-net-framework-4-6-1-offline-installer-for-windows
Dim oShell
set oShell = CreateObject("Wscript.Shell")
cd = (oShell.CurrentDirectory)
cmd = cd + "\DotNet\NDP461-KB3102436-x86-x64-AllOS-ENU.exe /norestart /passive /showrmui"
REM wscript.echo cmd
oShell.run cmd