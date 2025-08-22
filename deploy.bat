@echo off
echo ========================================
echo  AI Safety Jailbreak Detection
echo  Quick Deploy for Windows
echo ========================================
echo.

echo Step 1: Generating demo visualizations...
python scripts\visualize_results.py --demo --output-dir demo_plots
if %errorlevel% neq 0 (
    echo Error generating visualizations
    echo Try: python scripts\visualize_results.py --demo
    pause
    exit /b 1
)

echo.
echo Step 2: Starting local web server...
echo Your results will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python scripts\serve_results.py
pause