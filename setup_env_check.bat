@echo off
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Python Version:
python --version

echo.
echo Pip Version:
pip --version

echo.
echo Installed Packages:
pip list

echo.
echo Virtual Environment Location:
echo %VIRTUAL_ENV%

pause
