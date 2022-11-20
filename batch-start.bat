@echo off
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%~dp0
bcdedit >nul
if '%errorlevel%' NEQ '0' (goto UACPrompt) else (goto UACAdmin)
:UACPrompt
%1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&exit
exit /B
:UACAdmin
cd /d "%~dp0"
echo current Path=：%CD%
echo 已获取管理员权限

chcp 65001
D:
D:\e-projects\DouZero_For_HLDDZ_FullAuto
start python portal.py  1
start python portal.py  2
start python portal.py  3
