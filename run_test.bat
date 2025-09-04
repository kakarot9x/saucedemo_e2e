@echo off
rem This script automates the setup and testing process for a Python project.
rem It checks for Python, installs UV, syncs dependencies, and runs pytest.

rem =========================================================================
rem Step 1: Check if Python is installed and accessible in the system PATH.
rem This script assumes you have Python installed. If not, please download it
rem from python.org and ensure it is added to your PATH during installation.
rem =========================================================================
where python >nul 2>nul
if %errorlevel% neq 0 (
echo.
echo ERROR: Python is not found in your system's PATH.
echo Please install Python and ensure it is available in your command prompt.
echo For more information, visit https://www.python.org/downloads/
echo.
pause
exit /b 1
)

echo.
echo Found Python at:
where python
echo.

rem =========================================================================
rem Step 2: Install the 'uv' package manager using pipx.
rem pipx is the recommended way to install Python applications.
rem =========================================================================
echo Installing/updating uv...
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" >nul 2>nul
if %errorlevel% neq 0 (
echo ERROR: Failed to install or update UV.
echo.
pause
exit /b 1
)
echo.

rem =========================================================================
rem Step 3: Run uv sync to install/update all dependencies from pyproject.toml.
rem This command ensures all required packages are available in your
rem local project environment.
rem =========================================================================
echo Running 'uv sync' to install dependencies from pyproject.toml...
uv sync
if %errorlevel% neq 0 (
echo.
echo ERROR: 'uv sync' failed. Check for issues with your pyproject.toml.
echo.
pause
exit /b 1
)
echo.

rem =========================================================================
rem Step 4: Run the tests using pytest.
rem =========================================================================
echo Running tests with pytest...
uv run pytest %*
if %errorlevel% neq 0 (
echo.
echo Tests failed. See the output above for details.
echo.
pause
exit /b 1
)

rem =========================================================================
rem Script completed successfully
rem =========================================================================
echo.
echo All tasks completed successfully.
echo.

pause
exit /b 0