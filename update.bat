@echo off
chcp 65001 > nul
cd /d F:\Github\lungtundee

echo ===== Lungtundee Daily Update =====
echo.

echo [1/3] Fetching stock prices...
python fetch_prices.py
if errorlevel 1 (
    echo ERROR: fetch_prices.py failed
    pause
    exit /b 1
)

echo.
echo [2/3] Fetching fund NAVs...
python fetch_nav.py
if errorlevel 1 (
    echo ERROR: fetch_nav.py failed -- check API keys in .env
    echo        Continuing with existing NAV data...
)

echo.
echo [3/3] Generating dashboard...
python generate_dashboard.py
if errorlevel 1 (
    echo ERROR: generate_dashboard.py failed
    pause
    exit /b 1
)

echo.
echo ===== Done! Opening dashboard... =====
start "" portfolio_dashboard.html
