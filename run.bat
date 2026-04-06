@echo off
REM Claude Code Runner
REM Usage:
REM   run.bat "你好"                    - Run single prompt
REM   run.bat "你好" --continue         - Interactive mode
REM   run.bat --tui                     - TUI mode

if "%1"=="" (
    echo Usage: run.bat "your prompt" [--continue]
    echo        run.bat --tui
    exit /b 1
)

if "%1"=="--tui" (
    python -m claude_code
    exit /b %errorlevel%
)

REM Check for --continue flag
set "CONTINUE="
echo %* | findstr /C:"--continue" >nul
if %errorlevel%==0 set "CONTINUE=--continue"

REM Run claude-code
python -m claude_code main -p %*