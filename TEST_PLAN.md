# Test Plan for 3MF Texture Export Feature

## Overview
This test plan validates the texture export functionality added in version 1.1.3 of the Blender 3MF add-on.

## Test Environment Setup

### Prerequisites
- Blender 4.4+ installed
- 3MF add-on installed and enabled
- Sample textured models prepared
- 3MF viewer for validation (e.g., 3D Viewer on Windows, online 3MF viewers)

### Test Data Preparation
Create the following test assets in Blender:

1. **Simple Textured Cube**
   - UV-unwrapped cube
   - Single PNG texture (512x512)
   - Material with Principled BSDF + Image Texture node

2. **Multi-Object Scene**
   - 3 objects with different textures
   - 1 object with same texture as another (test texture reuse)

3. **Packed Texture Model**
   - Object with texture embedded in .blend file (File > External Data > Pack All)

4. **External Texture Model**
   - Object with texture referenced from external file

5. **No UV Map Model**
   - Object with material containing texture but no UV coordinates

6. **No Texture Model**
   - Object with material but no texture (color only)

---

## Test Cases

### Test Category 1: Basic Texture Export

#### TC-1.1: Export Single Textured Object (PNG)
**Objective**: Verify basic texture export with PNG image

**Steps**:
1. Open Blender and load the Simple Textured Cube
2. Go to File > Export > 3D Manufacturing Format (.3mf)
3. Choose export location
4. Click "Export 3MF"
5. Extract the exported .3mf file (it's a ZIP archive)
6. Verify file structure

**Expected Results**:
- ✅ Export completes without errors
- ✅ 3MF archive contains `/3D/Textures/` folder
- ✅ Texture image file exists in `/3D/Textures/`
- ✅ `3dmodel.model` contains `xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02"` namespace
- ✅ `texture2d` element exists with correct path and contenttype="image/png"
- ✅ `texture2dgroup` element exists with `tex2coord` children
- ✅ Object references texture2dgroup via `pid` attribute
- ✅ Triangles have `p1`, `p2`, `p3` attributes

**Validation Command** (Linux/Mac):
```bash
unzip -l exported_model.3mf | grep -i texture
```

---

#### TC-1.2: Export Single Textured Object (JPEG)
**Objective**: Verify texture export with JPEG image

**Steps**:
1. Create object with JPEG texture
2. Export to 3MF
3. Extract and verify

**Expected Results**:
- ✅ Texture exported with contenttype="image/jpeg"
- ✅ File extension is .jpg or .jpeg

---

#### TC-1.3: Export with Packed Texture
**Objective**: Verify packed images are extracted and exported

**Steps**:
1. Open model with packed texture (File > External Data > Pack All)
2. Export to 3MF
3. Extract and verify

**Expected Results**:
- ✅ Packed image is extracted to `/3D/Textures/`
- ✅ Image has appropriate filename
- ✅ Image data is correct (can be opened in image viewer)

---

#### TC-1.4: Export with External Texture
**Objective**: Verify external texture files are copied

**Steps**:
1. Open model with external texture file
2. Export to 3MF
3. Extract and verify

**Expected Results**:
- ✅ External texture is copied to `/3D/Textures/`
- ✅ Filename preserved or sanitized appropriately

---

### Test Category 2: Multiple Objects and Materials

#### TC-2.1: Export Multiple Objects with Different Textures
**Objective**: Verify multiple unique textures are exported

**Steps**:
1. Create scene with 3 objects, each with unique texture
2. Export to 3MF
3. Extract and verify

**Expected Results**:
- ✅ All 3 textures present in `/3D/Textures/`
- ✅ 3 separate `texture2d` resources created
- ✅ Each object has its own `texture2dgroup`
- ✅ Resource IDs are unique

---

#### TC-2.2: Export Multiple Objects with Same Texture
**Objective**: Verify texture reuse (single texture2d, multiple texture2dgroups)

**Steps**:
1. Create 2 objects with same texture but different UV layouts
2. Export to 3MF
3. Extract and verify

**Expected Results**:
- ✅ Only 1 texture file in archive (no duplication)
- ✅ Only 1 `texture2d` resource
- ✅ 2 separate `texture2dgroup` resources (per-mesh UV layouts)
- ✅ Both groups reference same `texid`

---

#### TC-2.3: Export Selection Only
**Objective**: Verify "Selection Only" export option

**Steps**:
1. Create scene with 3 textured objects
2. Select only 1 object
3. Export with "Selection Only" enabled
4. Verify

**Expected Results**:
- ✅ Only selected object's texture exported
- ✅ Other textures not included

---

### Test Category 3: Edge Cases and Fallback Behavior

#### TC-3.1: Export Object with Texture but No UV Map
**Objective**: Verify graceful fallback when UV coordinates missing

**Steps**:
1. Create object with textured material
2. Remove UV map from object
3. Export to 3MF
4. Check console for warnings

**Expected Results**:
- ✅ Export completes without crash
- ✅ Falls back to color-only export (basematerials)
- ✅ Warning logged: texture detected but no UV coordinates
- ✅ No texture2dgroup created for this object

---

#### TC-3.2: Export Object with Missing External Texture File
**Objective**: Verify handling of missing texture files

**Steps**:
1. Create object with external texture reference
2. Delete or move the texture file
3. Export to 3MF
4. Check console

**Expected Results**:
- ✅ Export completes without crash
- ✅ Warning logged: "Texture file not found: [path]"
- ✅ Object falls back to color-only export
- ✅ Other objects in scene export correctly

---

#### TC-3.3: Export Object with No Texture (Color Only)
**Objective**: Verify backward compatibility (existing behavior maintained)

**Steps**:
1. Create object with solid color material (no texture)
2. Export to 3MF
3. Verify

**Expected Results**:
- ✅ Export works as before
- ✅ Uses basematerials for color
- ✅ No texture resources created
- ✅ Material namespace may or may not be present (acceptable either way)

---

#### TC-3.4: Export Empty Scene
**Objective**: Verify handling of edge case

**Steps**:
1. Create new empty scene
2. Attempt export

**Expected Results**:
- ✅ Export completes
- ✅ No crash or errors
- ✅ Valid 3MF file created (even if empty)

---

### Test Category 4: UV Coordinate Accuracy

#### TC-4.1: Verify UV Mapping Correctness
**Objective**: Ensure UV coordinates are correctly exported

**Steps**:
1. Create cube with custom UV unwrap
2. Apply checkerboard texture
3. Export to 3MF
4. Import into 3MF viewer

**Expected Results**:
- ✅ Texture appears correctly mapped in viewer
- ✅ No visible distortion or incorrect mapping
- ✅ Checkerboard pattern aligns with geometry

**Manual Validation**:
- Compare Blender viewport with 3MF viewer side-by-side
- Verify texture orientation matches

---

#### TC-4.2: Complex UV Layout
**Objective**: Test complex UV unwrapping scenarios

**Steps**:
1. Create object with overlapping UVs or complex layout
2. Export and validate

**Expected Results**:
- ✅ All unique UV coordinates exported
- ✅ UV coordinate indices correctly reference tex2coord elements
- ✅ No data loss or corruption

---

### Test Category 5: Performance and Scale

#### TC-5.1: Large Texture (4K)
**Objective**: Verify handling of large texture files

**Steps**:
1. Apply 4096x4096 texture to object
2. Export to 3MF
3. Check file size and export time

**Expected Results**:
- ✅ Export completes successfully
- ✅ Large texture included in archive
- ✅ Reasonable export time (< 30 seconds for single object)

---

#### TC-5.2: Many Objects with Textures
**Objective**: Stress test with multiple textured objects

**Steps**:
1. Create scene with 20+ textured objects
2. Export to 3MF
3. Verify

**Expected Results**:
- ✅ All textures exported
- ✅ All texture2dgroups created
- ✅ No resource ID conflicts
- ✅ Reasonable export time

---

### Test Category 6: 3MF Specification Compliance

#### TC-6.1: XML Validation
**Objective**: Verify generated XML is valid

**Steps**:
1. Export textured model
2. Extract 3dmodel.model
3. Validate XML structure

**Expected Results**:
- ✅ Well-formed XML (no parse errors)
- ✅ Correct namespace declarations
- ✅ Material namespace: `xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02"`
- ✅ Elements use correct namespace prefixes (`m:texture2d`, `m:texture2dgroup`, `m:tex2coord`)

**Validation Method**:
```bash
xmllint --noout 3dmodel.model
```

---

#### TC-6.2: 3MF Viewer Compatibility
**Objective**: Verify exported files work in standard 3MF viewers

**Test Viewers**:
- Windows 3D Viewer (built-in)
- Online viewers (e.g., https://3dviewer.net)
- CAD software supporting 3MF (if available)

**Steps**:
1. Export textured model
2. Open in each viewer
3. Verify texture display

**Expected Results**:
- ✅ File opens without errors
- ✅ Texture displays correctly
- ✅ Colors and texture match Blender preview

---

### Test Category 7: Material Node Configurations

#### TC-7.1: Principled BSDF with Image Texture
**Objective**: Test standard material setup

**Steps**:
1. Create material: Principled BSDF → Base Color ← Image Texture
2. Export

**Expected Results**:
- ✅ Texture exported correctly

---

#### TC-7.2: Multiple Texture Nodes (First One Used)
**Objective**: Verify only first texture is exported (limitation)

**Steps**:
1. Create material with 2 Image Texture nodes
2. Export
3. Verify only first texture exported

**Expected Results**:
- ✅ Only first Image Texture node processed
- ✅ Other textures ignored (as per design)

---

#### TC-7.3: Procedural Texture (No Image)
**Objective**: Verify handling of procedural/generated textures

**Steps**:
1. Create material with only procedural textures (Noise, Voronoi, etc.)
2. Export

**Expected Results**:
- ✅ Falls back to color-only export
- ✅ No texture resources created
- ✅ Warning logged (if texture node detected but has no image)

---

### Test Category 8: Regression Tests

#### TC-8.1: Color-Only Export Still Works
**Objective**: Ensure new code doesn't break existing functionality

**Steps**:
1. Export model without textures (pre-existing test case)
2. Verify output matches expected format

**Expected Results**:
- ✅ Export works as before version 1.1.3
- ✅ Uses basematerials
- ✅ Colors preserved

---

#### TC-8.2: Import Still Works
**Objective**: Verify import functionality not affected

**Steps**:
1. Import existing 3MF file (without textures)
2. Verify import completes

**Expected Results**:
- ✅ Import works as before
- ✅ No errors or warnings related to texture code

---

## Automated Test Script (Python)

Since this is a Blender add-on, automated tests require Blender's Python environment. Here's a test script template:

```python
# test_texture_export.py
# Run with: blender --background --python test_texture_export.py

import bpy
import os
import zipfile
import xml.etree.ElementTree as ET

def setup_test_scene():
    """Create a simple textured cube for testing"""
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    
    # Create material with texture
    mat = bpy.data.materials.new(name="TestMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Add nodes
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    tex_node = nodes.new(type='ShaderNodeTexImage')
    output = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Link nodes
    mat.node_tree.links.new(tex_node.outputs[0], bsdf.inputs[0])
    mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
    
    # Create test texture
    img = bpy.data.images.new("TestTexture", width=512, height=512)
    tex_node.image = img
    
    # Assign material
    if cube.data.materials:
        cube.data.materials[0] = mat
    else:
        cube.data.materials.append(mat)
    
    return cube

def test_basic_export():
    """Test Case: Basic texture export"""
    print("\n=== Running Test: Basic Texture Export ===")
    
    cube = setup_test_scene()
    export_path = "/tmp/test_texture_export.3mf"
    
    # Export
    try:
        bpy.ops.export_mesh.threemf(filepath=export_path)
        print("✓ Export completed")
    except Exception as e:
        print(f"✗ Export failed: {e}")
        return False
    
    # Verify file exists
    if not os.path.exists(export_path):
        print("✗ Export file not created")
        return False
    print("✓ Export file created")
    
    # Verify archive structure
    try:
        with zipfile.ZipFile(export_path, 'r') as zf:
            files = zf.namelist()
            
            # Check for texture folder
            texture_files = [f for f in files if f.startswith('3D/Textures/')]
            if not texture_files:
                print("✗ No textures found in archive")
                return False
            print(f"✓ Found {len(texture_files)} texture(s)")
            
            # Check model file
            if '3D/3dmodel.model' not in files:
                print("✗ Model file missing")
                return False
            
            # Parse and validate XML
            with zf.open('3D/3dmodel.model') as model_file:
                tree = ET.parse(model_file)
                root = tree.getroot()
                
                # Check material namespace
                if 'http://schemas.microsoft.com/3dmanufacturing/material/2015/02' not in root.attrib.values():
                    print("⚠ Material namespace not found in root element")
                else:
                    print("✓ Material namespace present")
                
                # Check for texture2d elements
                ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/material/2015/02',
                      'core': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
                texture2d = root.findall('.//m:texture2d', ns)
                if not texture2d:
                    print("✗ No texture2d elements found")
                    return False
                print(f"✓ Found {len(texture2d)} texture2d element(s)")
                
                # Check for texture2dgroup
                texture2dgroup = root.findall('.//m:texture2dgroup', ns)
                if not texture2dgroup:
                    print("✗ No texture2dgroup elements found")
                    return False
                print(f"✓ Found {len(texture2dgroup)} texture2dgroup element(s)")
                
    except Exception as e:
        print(f"✗ Archive validation failed: {e}")
        return False
    
    print("✓ All checks passed")
    return True

def test_no_uv_fallback():
    """Test Case: Fallback when no UV coordinates"""
    print("\n=== Running Test: No UV Fallback ===")
    
    cube = setup_test_scene()
    
    # Remove UV map
    if cube.data.uv_layers:
        cube.data.uv_layers.remove(cube.data.uv_layers[0])
    
    export_path = "/tmp/test_no_uv.3mf"
    
    try:
        bpy.ops.export_mesh.threemf(filepath=export_path)
        print("✓ Export completed without crash")
        return True
    except Exception as e:
        print(f"✗ Export failed: {e}")
        return False

def run_all_tests():
    """Run all automated tests"""
    tests = [
        test_basic_export,
        test_no_uv_fallback,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*50)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    print("="*50)
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
```

**To run automated tests**:
```bash
blender --background --python test_texture_export.py
```

---

## Manual Testing Checklist

Use this checklist for manual testing:

- [ ] TC-1.1: Single textured object (PNG)
- [ ] TC-1.2: Single textured object (JPEG)
- [ ] TC-1.3: Packed texture export
- [ ] TC-1.4: External texture export
- [ ] TC-2.1: Multiple objects with different textures
- [ ] TC-2.2: Multiple objects with same texture
- [ ] TC-2.3: Selection only export
- [ ] TC-3.1: No UV map fallback
- [ ] TC-3.2: Missing texture file handling
- [ ] TC-3.3: Color-only export (no texture)
- [ ] TC-3.4: Empty scene export
- [ ] TC-4.1: UV mapping correctness
- [ ] TC-4.2: Complex UV layouts
- [ ] TC-5.1: Large texture (4K)
- [ ] TC-5.2: Many textured objects
- [ ] TC-6.1: XML validation
- [ ] TC-6.2: 3MF viewer compatibility
- [ ] TC-7.1: Principled BSDF + Image Texture
- [ ] TC-7.2: Multiple texture nodes
- [ ] TC-7.3: Procedural textures
- [ ] TC-8.1: Color-only regression
- [ ] TC-8.2: Import functionality

---

## Test Results Template

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| TC-1.1  | Single PNG texture | ⏳ Pending | |
| TC-1.2  | Single JPEG texture | ⏳ Pending | |
| ... | ... | ... | |

**Status Legend**:
- ⏳ Pending
- ✅ Passed
- ❌ Failed
- ⚠️ Passed with warnings

---

## Known Issues / Limitations

Document any known issues found during testing:

1. **Single Texture Per Material**: Only first Image Texture node exported (by design)
2. **Active UV Layer Only**: Other UV layers ignored (by design)
3. **No Import Support**: Texture import not implemented yet (future work)

---

## Success Criteria

The texture export feature is considered ready for release when:

- ✅ All critical test cases (TC-1.x, TC-2.x) pass
- ✅ Edge cases (TC-3.x) handle gracefully without crashes
- ✅ At least 2 different 3MF viewers display textures correctly
- ✅ No regressions in existing functionality
- ✅ XML validates against 3MF specification
- ✅ Automated tests pass (if implemented)

---

## Bug Reporting Template

If issues are found during testing:

**Title**: [Texture Export] Brief description

**Description**:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Blender version
- Test case ID

**Attachments**:
- Screenshots
- Sample .blend file
- Exported .3mf file
- Console output/logs
