@echo off
chcp 65001 >nul
:: ============================================================================
:: PDF Compressor Pro - Batch Interface
:: ============================================================================
:: Provides a user-friendly menu to access the advanced features of the
:: pdf_compressor.py script, including the new compression modes.
:: ============================================================================

:: --- Configuration and Setup ---
title PDF Compressor Pro
color 0A
setlocal

SET "PYTHON_VENV_PATH=%~dp0.venv\Scripts\python.exe"
SET "COMPRESSOR_SCRIPT=%~dp0pdf_compressor.py"

:: --- Initial Checks ---
if not exist "%PYTHON_VENV_PATH%" (
    cls
    echo.
    echo  ERROR: Python virtual environment not found.
    echo  ---------------------------------------------
    echo  Expected to find it at: "%PYTHON_VENV_PATH%"
    echo  Please run `python -m venv .venv` to create it first.
    echo.
    pause
    exit /b 1
)

:start
cls
:: --- ASCII Art Logo ---
echo.
color 0C
echo ██  ███████╗ █████╗ ███████╗███████╗    ██████╗ ██████╗ ███████╗
color 0E
echo     ██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔══██╗██╔════╝
color 0A
echo ██╗ ███████╗███████║█████╗  █████╗      ██████╔╝██║  ██║█████╗
color 0B
echo ██║ ╚════██║██╔══██║██╔══╝  ██╔══╝      ██╔═══╝ ██║  ██║██╔══╝
color 09
echo ██║ ███████║██║  ██║██║     ███████╗    ██║     ██████╔╝██║
color 0D
echo ╚═╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚═╝     ╚═════╝ ╚═╝
                                        
echo.
color 0A
echo ================================================================================
echo                  iSafe PDF - The Ultimate PDF Tool by Ali Goodarzi
echo ================================================================================
echo.

:: --- Get User Input ---
set "PDF_PATH="
set /p "PDF_PATH=Enter the full path to your PDF file and press Enter: "

:: Remove quotes if user added them by dragging/dropping
set PDF_PATH=%PDF_PATH:"=%

if not exist "%PDF_PATH%" (
    echo.
    echo  ERROR: File not found. Please check the path and try again.
    echo.
    pause
    goto start
)

:menu
cls
echo ================================================================================
echo  Selected File: %PDF_PATH%
echo ================================================================================
echo.
echo  Choose Compression Mode:
echo  ------------------------
echo  [1] Smart Mode (RECOMMENDED)
echo      - Perfect for text documents or mixed PDFs (text + images).
echo      - Preserves 100%% text quality by only compressing images.
echo.
echo  [2] Aggressive Mode
echo      - Best for scanned documents or PDFs that are 100%% images.
echo      - Converts every page to a compressed image for maximum size reduction.
echo.
echo  [3] Go Back
echo.
set /p "MODE_CHOICE=Enter your choice (1-3): "

if "%MODE_CHOICE%"=="1" set MODE=smart
if "%MODE_CHOICE%"=="2" set MODE=aggressive
if "%MODE_CHOICE%"=="3" goto start
if not defined MODE (
    echo Invalid choice. Please try again.
    pause
    goto menu
)

:profile_menu
cls
echo ================================================================================
echo  Selected File: %PDF_PATH%
echo  Mode: %MODE%
echo ================================================================================
echo.
echo  Choose a Compression Profile:
echo  -----------------------------
echo  [1] Low Quality    (Smallest file size)
echo  [2] Medium Quality (Balanced size and quality) - RECOMMENDED
echo  [3] High Quality   (Better image quality)
echo  [4] Best Quality   (Minimal compression)
echo.
echo  [5] Go Back
echo.
set /p "PROFILE_CHOICE=Enter your choice (1-5): "

if "%PROFILE_CHOICE%"=="1" set PROFILE=low
if "%PROFILE_CHOICE%"=="2" set PROFILE=medium
if "%PROFILE_CHOICE%"=="3" set PROFILE=high
if "%PROFILE_CHOICE%"=="4" set PROFILE=best
if "%PROFILE_CHOICE%"=="5" goto menu
if not defined PROFILE (
    echo Invalid choice. Please try again.
    pause
    goto profile_menu
)

:: --- Execute Compression ---
cls
echo.
echo  Initializing Compression...
echo  ---------------------------
echo  - Mode:    %MODE%
echo  - Profile: %PROFILE%
echo.
echo  Please wait, this may take a moment...
echo.

"%PYTHON_VENV_PATH%" "%COMPRESSOR_SCRIPT%" "%PDF_PATH%" --mode %MODE% --profile %PROFILE%

echo.
echo ================================================================================
echo  Compression task finished. Check the output above for results.
echo ================================================================================
echo.
echo  Press any key to return to the main menu...
pause >nul
goto start
