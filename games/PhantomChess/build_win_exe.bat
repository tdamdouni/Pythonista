echo Building Simple.exe..
DEL /Q Simple.exe
pyinstaller Phantom\Run_this.py -F --icon=icon.ico
echo Done, cleaning up...
move /Y dist\Run_this.exe Simple.exe
rd /S /Q dist
rd /S /Q build
DEL /Q Run_this.spec
echo Complete!
