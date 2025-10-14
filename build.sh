#!/bin/bash
# Build script for creating a PyInstaller executable

set -e

echo "Building CVASL GUI executable with PyInstaller..."

# Clean previous builds
if [ -d "build" ]; then
    echo "Cleaning build directory..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "Cleaning dist directory..."
    rm -rf dist
fi

# Run PyInstaller
echo "Running PyInstaller..."
poetry run pyinstaller cvasl-gui.spec

echo ""
echo "Build complete!"
echo "Executable can be found in: dist/cvasl-gui/"
echo ""
echo "To run the application:"
echo "  cd dist/cvasl-gui"
echo "  ./cvasl-gui"
