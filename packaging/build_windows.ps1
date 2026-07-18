$ErrorActionPreference = "Stop"

Write-Host "Installing/updating GUI and packaging dependencies..."
python -m pip install -r requirements-gui.txt
python -m pip install pyinstaller

Write-Host "Cleaning previous PyInstaller output..."
Remove-Item .\build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\dist -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Building WordIndexer desktop application..."
pyinstaller `
    --noconfirm `
    --clean `
    WordIndexer.spec

if (-not (Test-Path .\dist\WordIndexer\WordIndexer.exe)) {
    throw "PyInstaller did not create dist\WordIndexer\WordIndexer.exe"
}

Write-Host "PyInstaller build completed."
Write-Host "Executable: dist\WordIndexer\WordIndexer.exe"
Write-Host "Next: open installer\WordIndexer.iss in Inno Setup and click Compile."
