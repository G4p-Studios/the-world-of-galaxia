@echo off
mkdir release
mkdir release\twg
"C:\Program Files (x86)\BGT\bgt.exe" -Ctwg.bgt
move twg.exe release\twg\
xcopy /E /I libraries release\twg\libraries
copy changelog.txt release\twg\
copy keyconfig.ini release\twg\
powershell -command "Compress-Archive -Path 'release\twg\' -DestinationPath 'release\twg.zip' -Force"
rmdir /S /Q release\twg
pyinstaller --windowed --onefile unzip.py
copy dist\unzip.exe release\unzip.exe
rmdir /s/q build dist
del unzip.spec