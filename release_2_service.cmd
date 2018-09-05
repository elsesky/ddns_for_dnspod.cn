@REM python Pypod_service.py install 
@start /b python setup_service.py py2exe
@start /b python setup_service_d.py py2exe
@start /b python setup_pylistpod.py py2exe
python setup_uilistpod.py py2exe
@del /f  /q .\dist\w9xpopen.exe