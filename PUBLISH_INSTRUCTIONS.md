# Publishing simplesitesearch to PyPI

This document provides step-by-step instructions for building and publishing the `simplesitesearch` package to PyPI.

## Prerequisites

1. **Python 3.8+** installed on your system
2. **pip** package manager
3. **PyPI account** - Create one at https://pypi.org/account/register/

## Step 1: Version and Git (before building)

1. Ensure version is set to the same value in:
   - `simplesitesearch/__init__.py` (`__version__`)
   - `setup.py` (`version=`)
   - `pyproject.toml` (`version =` under `[project]`)
2. Commit changes and tag the release:
   ```bash
   git add -A && git status
   git commit -m "Release 0.0.3"
   git tag v0.0.3
   ```

## Step 2: Build the Package

### Option A: Using the build script (Recommended)
```bash
cd /path/to/simplesitesearch   # e.g. /Users/flavien/workspace/simplesitesearch
chmod +x build_and_publish.sh
./build_and_publish.sh
```

### Option B: Manual build
```bash
cd /path/to/simplesitesearch

# Install build tools
python3 -m pip install --upgrade build twine

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python3 -m build

# Test the package (replace 0.0.3 with current version if different)
python3 -m pip install dist/simplesitesearch-0.0.3-py3-none-any.whl --force-reinstall
```

## Step 3: Set up PyPI Authentication

### Create API Token
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name (e.g., "simplesitesearch")
4. Set scope to "Entire account" (for first upload) or "Specific project" (for updates)
5. Copy the token (starts with `pypi-`)

### Configure credentials
Create `~/.pypirc` file:
```ini
[pypi]
username = __token__
password = pypi-your-api-token-here
```

**Important**: Replace `pypi-your-api-token-here` with your actual token.

## Step 4: Upload to PyPI

### Upload the package
```bash
twine upload dist/*
```

### Verify upload
1. Go to https://pypi.org/project/simplesitesearch/
2. Check that the new version (e.g. 0.0.3) is listed
3. Test installation: `pip install simplesitesearch`

## Step 5: Test Installation

### Test from PyPI
```bash
# Create a new virtual environment
python3 -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install simplesitesearch

# Test import
python3 -c "import simplesitesearch; print(f'Version: {simplesitesearch.__version__}')"
```

## Package Information

- **Package Name**: `simplesitesearch`
- **Current version**: see `simplesitesearch/__init__.py` (e.g. 0.0.3)
- **PyPI URL**: https://pypi.org/project/simplesitesearch/
- **Installation**: `pip install simplesitesearch`

## Troubleshooting

### Common Issues

1. **"Package already exists"**
   - You may be re-uploading the same version; bump the version and rebuild
   - Or try a different name in `setup.py` and `pyproject.toml`

2. **"Authentication failed"**
   - Check your API token in `~/.pypirc`
   - Ensure the token has the correct permissions

3. **"Build failed"**
   - Check that all required files are present
   - Run `python3 test_package.py` to verify structure

4. **"Import failed after installation"**
   - Check that `__init__.py` files are present
   - Verify package structure matches the import statements

### File Structure Verification
Ensure your package has this structure:
```
simplesitesearch/
├── simplesitesearch/
│   ├── __init__.py
│   ├── views.py
│   ├── utils.py
│   ├── urls.py
│   ├── cms_apps.py
│   └── templates/
│       └── simplesitesearch/
│           ├── pagination.html
│           └── search_results.html
├── setup.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Updating the Package

For future updates:

1. Bump version in `simplesitesearch/__init__.py`, `setup.py`, and `pyproject.toml` (same value in all three).
2. Update the **Changelog** in `README.md`.
3. Commit and tag: `git commit -m "Release X.Y.Z"` then `git tag vX.Y.Z`.
4. Rebuild: `python3 -m build`
5. Upload: `twine upload dist/*`
6. Push to Git and publish tags: `git push origin main && git push origin --tags` (adjust `main` for your default branch)

## Support

If you encounter issues:
1. Check the PyPI documentation: https://packaging.python.org/
2. Verify your package structure matches the requirements
3. Test locally before uploading




