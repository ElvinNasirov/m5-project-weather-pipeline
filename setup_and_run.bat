@echo off
echo ================================
echo Weather Pipeline Setup and Run
echo ================================

echo.
echo Step 1: Creating virtual environment...
python -m venv .venv

echo.
echo Step 2: Activating virtual environment...
call .venv\Scripts\activate

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing project requirements...
pip install -r requirements.txt

echo.
echo Step 5: Running full weather pipeline...
python src\pipeline.py

echo.
echo ================================
echo Pipeline finished.
echo ================================

pause