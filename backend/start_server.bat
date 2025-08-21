@echo off
echo Installing Python dependencies for Medical Diagnosis API...
pip install -r requirements.txt

echo.
echo Starting the Medical Diagnosis API server...
echo The server will be available at http://localhost:8000
echo.
python main.py
