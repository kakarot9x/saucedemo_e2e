    @echo off
    echo Setting up uv virtual environment...

    rem Install uv if not already installed
    where uv >nul 2>nul
    if %errorlevel% neq 0 (
        echo uv not found. Installing uv...
        pip install uv
    )

    rem Create the virtual environment named 'venv'
    uv venv venv

    rem Activate the virtual environment
    echo Activating virtual environment...
    call .\venv\Scripts\activate.bat

    echo Virtual environment 'venv' created and activated.
    echo You are now in the virtual environment.