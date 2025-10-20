@echo off
REM Comprehensive test runner for Retail Customer Segmentation POC
REM Run this from the project root directory

echo ============================================================
echo Retail Customer Segmentation POC - Full Test Suite
echo ============================================================
echo.

cd /d %~dp0

echo [1/7] Testing Configuration Loading...
python examples\test_config.py
if errorlevel 1 (
    echo FAILED: Configuration test failed
    pause
    exit /b 1
)
echo PASSED: Configuration loaded successfully
echo.

echo [2/7] Testing Persona Generation...
python examples\test_persona_generation.py
if errorlevel 1 (
    echo FAILED: Persona generation test failed
    pause
    exit /b 1
)
echo PASSED: Persona generation works
echo.

echo [3/7] Validating Persona Distribution...
python examples\validate_persona_distribution.py
if errorlevel 1 (
    echo FAILED: Persona distribution validation failed
    pause
    exit /b 1
)
echo PASSED: Persona distribution validated
echo.

echo [4/7] Generating Customer Data...
python examples\generate_customer_data.py
if errorlevel 1 (
    echo FAILED: Customer data generation failed
    pause
    exit /b 1
)
echo PASSED: Customer data generated
echo.

echo [5/7] Running GMM Clustering...
python examples\run_gmm_clustering.py
if errorlevel 1 (
    echo FAILED: GMM clustering failed
    pause
    exit /b 1
)
echo PASSED: GMM clustering completed
echo.

echo [6/7] Running Full Segmentation Pipeline...
python examples\run_segmentation_pipeline.py
if errorlevel 1 (
    echo FAILED: Segmentation pipeline failed
    pause
    exit /b 1
)
echo PASSED: Full pipeline completed
echo.

echo [7/7] Generating Visualizations...
python examples\visualize_segments.py
if errorlevel 1 (
    echo FAILED: Visualization generation failed
    pause
    exit /b 1
)
echo PASSED: Visualizations generated
echo.

echo ============================================================
echo ALL TESTS PASSED!
echo ============================================================
echo.
echo Generated outputs:
echo   - data\customer_sales_data_basic.csv
echo   - data\customer_sales_data_enriched.csv
echo   - data\output\*.json (cluster profiles)
echo   - visualizations\*.png (all plots)
echo.
pause
