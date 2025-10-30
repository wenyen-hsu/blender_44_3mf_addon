# Quick Test Reference Card

## 🚀 Quick Start

```bash
# Run all automated tests
./run_tests.sh

# Or run directly with Blender
blender --background --python test_texture_export.py
```

## 📋 5-Minute Smoke Test

Quick validation that texture export is working:

1. **Create Test Model**
   ```
   - Open Blender
   - Create cube (Shift+A > Mesh > Cube)
   - Unwrap UVs (Tab > U > Unwrap)
   - Add material with texture:
     * Shading workspace
     * Add Image Texture node
     * Connect to Principled BSDF Base Color
     * Load any PNG/JPEG image
   ```

2. **Export**
   ```
   - File > Export > 3D Manufacturing Format (.3mf)
   - Save as test.3mf
   ```

3. **Verify**
   ```bash
   # Extract and check
   unzip -l test.3mf | grep -i texture
   # Should see: 3D/Textures/[your-image-name]
   
   # Check XML
   unzip -p test.3mf 3D/3dmodel.model | grep texture2d
   # Should see: <m:texture2d ...
   ```

4. **View**
   ```
   - Open test.3mf in 3D Viewer (Windows)
   - Or upload to: https://3dviewer.net
   - Texture should display on model
   ```

## ✅ Expected Test Results

### Automated Tests (5 tests)
All should pass:
```
✓ PASS: TC-1.1: Basic Texture Export (PNG)
✓ PASS: TC-3.1: No UV Map Fallback
✓ PASS: TC-8.1: Color-Only Export (Regression)
✓ PASS: TC-2.1: Multiple Objects with Different Textures
✓ PASS: TC-6.1: XML Validation
```

### Archive Structure
```
test.3mf
├── 3D/
│   ├── 3dmodel.model       ← Contains texture references
│   └── Textures/
│       └── texture.png     ← Your texture image
├── [Content_Types].xml
└── _rels/
    └── .rels
```

### XML Content
Should contain:
```xml
<model xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02">
  <resources>
    <m:texture2d id="2" path="/3D/Textures/..." contenttype="image/png"/>
    <m:texture2dgroup id="3" texid="2">
      <m:tex2coord u="..." v="..."/>
      ...
    </m:texture2dgroup>
    <object id="4" pid="3" pindex="0">
      ...
      <triangle v1="0" v2="1" v3="2" p1="0" p2="1" p3="2"/>
    </object>
  </resources>
</model>
```

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| No texture in archive | Check material has Image Texture node with image loaded |
| No texture displayed in viewer | Verify object has UV map (Edit mode > UV > Unwrap) |
| "Blender not found" error | Install Blender 4.4+ or add to PATH |
| Tests fail to import `bpy` | Must run with `blender --python`, not standalone python |
| Export has no texture2d elements | Check material uses nodes (Use Nodes enabled) |

## 📊 Test Coverage Summary

| Category | Automated | Manual | Total |
|----------|-----------|--------|-------|
| Basic Export | 1 | 3 | 4 |
| Multiple Objects | 1 | 2 | 3 |
| Edge Cases | 2 | 2 | 4 |
| Other | 1 | 8 | 9 |
| **TOTAL** | **5** | **15** | **20** |

## 📚 Full Documentation

- **TESTING.md** - Complete testing guide
- **TEST_PLAN.md** - All 22 test cases with detailed procedures
- **TEXTURE_IMPLEMENTATION.md** - Technical implementation details

## 🎯 Success Criteria

✅ All 5 automated tests pass  
✅ Texture files appear in 3MF archive  
✅ XML contains texture2d and texture2dgroup elements  
✅ Textures display correctly in 3MF viewers  
✅ No regressions in color-only export  

## 📝 Report Issues

If you find a bug:
1. Note which test case failed (TC-X.X)
2. Capture console output
3. Save the .blend file
4. Save the exported .3mf file
5. Report with test case ID and files

---

**Version**: 1.1.3  
**Last Updated**: 2025-10-30  
**Automated Tests**: 5/5 implemented  
