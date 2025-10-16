#!/bin/bash
# Verification script to check the Python environment setup

echo "=== Retail Customer Categorization - Environment Verification ==="
echo ""

# Check directory structure
echo "✓ Checking directory structure..."
if [ -d "notebooks" ] && [ -d "data" ] && [ -d "src" ] && [ -d "tests" ] && [ -d "config" ] && [ -d "models" ]; then
    echo "  ✓ All directories present"
else
    echo "  ✗ Missing directories"
    exit 1
fi

# Check configuration files
echo "✓ Checking configuration files..."
if [ -f "environment.yml" ] && [ -f "requirements.txt" ] && [ -f "pyproject.toml" ]; then
    echo "  ✓ All configuration files present"
else
    echo "  ✗ Missing configuration files"
    exit 1
fi

# Check notebooks
echo "✓ Checking Jupyter notebooks..."
notebook_count=$(ls notebooks/*.ipynb 2>/dev/null | wc -l)
if [ $notebook_count -eq 3 ]; then
    echo "  ✓ Found $notebook_count notebooks"
else
    echo "  ✗ Expected 3 notebooks, found $notebook_count"
    exit 1
fi

# Check README files
echo "✓ Checking documentation..."
readme_count=$(find . -name "README.md" | wc -l)
if [ $readme_count -ge 5 ]; then
    echo "  ✓ Found $readme_count README files"
else
    echo "  ✗ Expected at least 5 README files, found $readme_count"
fi

# Check Python package structure
echo "✓ Checking Python package structure..."
if [ -f "src/retail_customer_cat/__init__.py" ]; then
    echo "  ✓ Package __init__.py present"
else
    echo "  ✗ Missing package __init__.py"
    exit 1
fi

# Test Python package import
echo "✓ Testing Python package import..."
if cd src && python -c "import retail_customer_cat; print('  Package version: ' + retail_customer_cat.__version__)" 2>/dev/null && cd ..; then
    echo "  ✓ Package imports successfully"
else
    echo "  ✗ Package import failed"
    exit 1
fi

# Check .gitkeep files
echo "✓ Checking .gitkeep files..."
gitkeep_count=$(find . -name ".gitkeep" | wc -l)
if [ $gitkeep_count -ge 4 ]; then
    echo "  ✓ Found $gitkeep_count .gitkeep files"
else
    echo "  ✗ Expected at least 4 .gitkeep files"
fi

echo ""
echo "=== Verification Complete ==="
echo ""
echo "Next steps:"
echo "1. Create conda environment: conda env create -f environment.yml"
echo "2. Activate environment: conda activate retail_customer_cat"
echo "3. Launch Jupyter: jupyter lab"
echo ""
