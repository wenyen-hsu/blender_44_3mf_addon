# Testing the 3MF Texture Export Feature

## Overview

This directory contains comprehensive tests for the texture export functionality added in version 1.1.3.

## Test Files

1. **TEST_PLAN.md** - Comprehensive test plan with manual test cases
2. **test_texture_export.py** - Automated test script (requires Blender)
3. **run_tests.sh** - Shell script to run automated tests

## Quick Start

### Running Automated Tests

#### Prerequisites
- Blender 4.4+ installed and in your PATH
- 3MF add-on installed in Blender

#### Run Tests

**Linux/macOS:**
```bash
./run_tests.sh
```

**Manual execution:**
```bash
blender --background --python test_texture_export.py
```

**Windows:**
```cmd
blender.exe --background --python test_texture_export.py
```

### Test Output

The automated tests will:
- Create test scenes programmatically
- Export to 3MF format
- Validate archive structure
- Check XML content
- Verify texture files are present

Example output:
```
======================================================================
3MF Texture Export - Automated Test Suite
======================================================================

[1/5] Running: Basic Export
----------------------------------------------------------------------
✓ PASS: TC-1.1: Basic Texture Export (PNG)
   Exported successfully with 1 texture(s)

[2/5] Running: No UV Fallback
----------------------------------------------------------------------
✓ PASS: TC-3.1: No UV Map Fallback
   Export completed without crash (graceful fallback)

...

======================================================================
TEST SUMMARY
======================================================================
✓ PASS: TC-1.1: Basic Texture Export (PNG)
✓ PASS: TC-3.1: No UV Map Fallback
✓ PASS: TC-8.1: Color-Only Export (Regression)
✓ PASS: TC-2.1: Multiple Objects with Different Textures
✓ PASS: TC-6.1: XML Validation

======================================================================
Results: 5/5 tests passed (100%)
======================================================================
```

## Manual Testing

For comprehensive manual testing, follow the test cases in **TEST_PLAN.md**:

### Key Test Scenarios

1. **Basic Texture Export** (TC-1.x)
   - Single textured object with PNG
   - Single textured object with JPEG
   - Packed vs external textures

2. **Multiple Objects** (TC-2.x)
   - Different textures per object
   - Same texture shared across objects
   - Selection-only export

3. **Edge Cases** (TC-3.x)
   - Objects without UV maps
   - Missing texture files
   - Color-only materials

4. **Validation** (TC-6.x)
   - 3MF viewer compatibility
   - XML structure compliance

### Manual Test Checklist

Use this checklist when testing manually:

```
□ Create UV-unwrapped cube with PNG texture
□ Export to 3MF
□ Extract archive and verify:
  □ Texture file in 3D/Textures/
  □ 3dmodel.model contains texture2d element
  □ 3dmodel.model contains texture2dgroup element
  □ Triangles have p1/p2/p3 attributes
□ Open in 3MF viewer (e.g., Windows 3D Viewer)
□ Verify texture displays correctly
```

## Test Results

Document your test results in TEST_PLAN.md under "Test Results Template" section.

## Troubleshooting

### Blender Not Found
```
ERROR: Blender not found in PATH
```
**Solution**: Install Blender or add it to your PATH

### Import Error
```
ModuleNotFoundError: No module named 'bpy'
```
**Solution**: Run the test using `blender --background --python` (not standalone Python)

### Export Fails
```
RuntimeError: Operator export_mesh.threemf not available
```
**Solution**: Ensure the 3MF add-on is installed and enabled in Blender

## Adding New Tests

To add new automated tests:

1. Open `test_texture_export.py`
2. Add a new test function following the pattern:
```python
def test_my_new_feature():
    """Test Case X.X: Description"""
    test_name = "TC-X.X: My New Test"
    
    try:
        # Setup test
        # Perform action
        # Verify result
        log_test(test_name, True, "Success message")
        return True
    except Exception as e:
        log_test(test_name, False, f"Exception: {str(e)}")
        return False
```
3. Add to `tests` list in `run_all_tests()`

## Continuous Integration

To integrate with CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run 3MF Tests
  run: |
    sudo apt-get install -y blender
    ./run_tests.sh
```

## Support

If you encounter issues:
1. Check test logs in `test_output.log`
2. Review TEST_PLAN.md for detailed test descriptions
3. Report bugs with test case ID and console output
