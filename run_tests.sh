#!/bin/bash
# Test runner script for 3MF texture export tests
# This script helps run the automated tests

set -e

echo "=========================================="
echo "3MF Texture Export Test Runner"
echo "=========================================="
echo ""

# Check if Blender is installed
if ! command -v blender &> /dev/null; then
    echo "ERROR: Blender not found in PATH"
    echo "Please install Blender 4.4+ or add it to your PATH"
    echo ""
    echo "On Ubuntu/Debian: sudo apt install blender"
    echo "On macOS: brew install blender"
    echo "Or download from: https://www.blender.org/download/"
    exit 1
fi

# Get Blender version
BLENDER_VERSION=$(blender --version | head -n 1)
echo "Found: $BLENDER_VERSION"
echo ""

# Check if test script exists
if [ ! -f "test_texture_export.py" ]; then
    echo "ERROR: test_texture_export.py not found"
    echo "Please run this script from the add-on directory"
    exit 1
fi

echo "Running automated tests..."
echo "=========================================="
echo ""

# Run tests
if blender --background --python test_texture_export.py 2>&1 | tee test_output.log; then
    echo ""
    echo "=========================================="
    echo "✓ Tests completed successfully"
    echo "=========================================="
    exit 0
else
    echo ""
    echo "=========================================="
    echo "✗ Tests failed - check test_output.log for details"
    echo "=========================================="
    exit 1
fi
