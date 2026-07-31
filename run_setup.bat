@echo off
REM Setup Script for NER Extraction Project
REM Runs on M drive - All files stay on M drive

setlocal enabledelayexpansion

echo.
echo ========================================
echo   NER Extraction Project - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Set working directory
cd /d "M:\MCHINE LERNING\Project one"

REM Set environment variables for M drive
set HF_HOME=M:\MCHINE LERNING\Project one\models
set TRANSFORMERS_CACHE=M:\MCHINE LERNING\Project one\models\transformers
set HF_DATASETS_CACHE=M:\MCHINE LERNING\Project one\models\datasets

echo Step 1: Installing Python dependencies...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Creating directories...
if not exist data mkdir data
if not exist models mkdir models

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Download model to M drive:
echo    python scripts/download_model.py
echo.
echo 2. Fine-tune the model:
echo    python scripts/fine_tune.py
echo.
echo 3. Start the API server:
echo    python scripts/api_server.py
echo.
echo 4. (Optional) Start the frontend:
echo    cd frontend
echo    npm install
echo    npm run dev
echo.
echo All files are saved to M drive (not C drive)
echo.
pause
