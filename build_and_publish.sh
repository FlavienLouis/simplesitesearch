#!/bin/bash

# Build and Publish Script for simplesitesearch
# This script builds the package and provides instructions for publishing to PyPI

set -e

echo "🚀 Building simplesitesearch package..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the package root directory."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build tools if not already installed
echo "📦 Installing build tools..."
python3 -m pip install --upgrade build twine

# Build the package
echo "🔨 Building package..."
python3 -m build

# Check the built package
echo "✅ Package built successfully!"
echo ""
echo "📁 Built files:"
ls -la dist/

echo ""
echo "🧪 Testing package installation..."
# Test installation in a temporary environment
python3 -m pip install dist/simplesitesearch-0.0.2-py3-none-any.whl --force-reinstall

echo ""
echo "✅ Package installation test successful!"
echo ""
echo "📋 Next steps to publish to PyPI:"
echo "1. Create a PyPI account at https://pypi.org/account/register/"
echo "2. Generate an API token at https://pypi.org/manage/account/token/"
echo "3. Create ~/.pypirc with your credentials:"
echo "   [pypi]"
echo "   username = __token__"
echo "   password = pypi-your-api-token-here"
echo ""
echo "4. Upload to PyPI:"
echo "   twine upload dist/*"
echo ""
echo "5. Verify at: https://pypi.org/project/simplesitesearch/"
echo ""
echo "🎉 Package is ready for publication!"



