@echo off
echo ================================
echo Running Weather Pipeline
echo ================================

call .venv\Scripts\activate

python src\pipeline.py

echo.
echo Pipeline finished.

pause