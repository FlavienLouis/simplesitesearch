#!/usr/bin/env python3
"""
Simple test script to verify the package structure and imports.
"""

import os
import sys

def test_package_structure():
    """Test that all required files exist."""
    required_files = [
        'setup.py',
        'setup.cfg',
        'pyproject.toml',
        'MANIFEST.in',
        'README.md',
        'LICENSE',
        'simplesitesearch/__init__.py',
        'simplesitesearch/views.py',
        'simplesitesearch/urls.py',
        'simplesitesearch/cms_apps.py',
        'simplesitesearch/templates/simplesitesearch/pagination.html',
        'simplesitesearch/templates/simplesitesearch/search_results.html',
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True


def test_imports():
    """Test that the package can be imported."""
    try:
        # Add current directory to path
        sys.path.insert(0, '.')

        # Test basic import
        import simplesitesearch
        print(f"✅ Package imported successfully, version: {simplesitesearch.__version__}")

        # Test submodule imports
        from simplesitesearch import views, urls, cms_apps
        print("✅ All submodules imported successfully")

        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing simplesitesearch package...")
    print("=" * 50)

    structure_ok = test_package_structure()
    print()

    import_ok = test_imports()
    print()

    if structure_ok and import_ok:
        print("🎉 Package structure and imports are working correctly!")
        print("\nNext steps:")
        print("1. Build the package: python -m build")
        print("2. Test installation: pip install dist/simplesitesearch-0.0.2-py3-none-any.whl")
        print("3. Upload to PyPI: twine upload dist/*")
        return True
    else:
        print("❌ Package has issues that need to be fixed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
