@echo off
echo are you sure do this ? yes or no
set /p input=
if "%input%" == "yes" (pause) else (exit)
rd /s/q _pycache__
rd /s/q build
rd /s/q dist
del *.spec
pyinstaller -i main.ico main.py
copy config.conf.prod dist\main\config.conf
exit