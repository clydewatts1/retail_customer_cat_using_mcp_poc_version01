@echo off
REM Quick validation test - runs fastest tests only
REM Run this from the project root directory

echo ============================================================
echo Quick Validation Test
echo ============================================================
echo.

cd /d %~dp0

echo [1/3] Testing Configuration...
python examples\test_config.py
if errorlevel 1 (
    echo FAILED
    pause
    exit /b 1
)
echo PASSED
echo.

echo [2/3] Testing Persona Generation...
python examples\test_persona_generation.py
if errorlevel 1 (
    echo FAILED
    pause
    exit /b 1
)
echo PASSED
echo.

echo [3/3] Validating Persona Distribution...
python examples\validate_persona_distribution.py
if errorlevel 1 (
    echo FAILED
    pause
    exit /b 1
)
echo PASSED
echo.

echo ============================================================
echo QUICK VALIDATION PASSED!
echo ============================================================
pause
