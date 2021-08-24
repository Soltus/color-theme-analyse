@echo off
cls
set self=%~dp0
@REM MMCQsc.cmd 文件所在路径
cd /d %self%
echo %self%
for /f %%a in (".") do set parent=%%~dpa
set python=%parent%python-3.9.6-embed-win32\python.exe
set main=%self%MMCQsc\scp\main.py
wt.exe -f %python% %main%
@REM cd ..\python-3.9.6-embed-win32
@REM .\python.exe ..\src\MMCQsc\scp\main.py
pause