# 3MF Texture Export Implementation

## Overview
This document describes the texture export functionality added to the Blender 3MF add-on.

## What Was Implemented

### 1. Texture Detection
The exporter now scans all materials in the scene for image texture nodes (TEX_IMAGE type). When found, these textures are:
- Extracted from the material node tree
- Written to the 3MF archive in the `/3D/Textures/` folder
- Registered as `texture2d` resources in the 3MF XML

### 2. Supported Texture Sources
- **Packed Images**: Images embedded in the .blend file
- **External Images**: Referenced image files on disk
- **Formats**: PNG and JPEG

### 3. UV Coordinate Export
For each mesh with textures:
- UV coordinates are extracted from the active UV layer
- Unique UV coordinates are collected and indexed
- A `texture2dgroup` resource is created per mesh
- Each unique UV coordinate becomes a `tex2coord` element

### 4. Triangle-Texture Mapping
Triangles reference texture coordinates using:
- `p1`, `p2`, `p3` attributes (indices into the texture2dgroup)
- Each corner of the triangle maps to its corresponding UV coordinate

## File Structure

When a textured model is exported, the 3MF archive contains:

```
model.3mf
├── 3D/
│   ├── 3dmodel.model          # Main model file with texture references
│   └── Textures/
│       ├── texture1.png        # Extracted texture images
│       └── texture2.jpg
├── [Content_Types].xml
└── _rels/
    └── .rels
```

## XML Structure

The 3dmodel.model file includes:

```xml
<model xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
       xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02">
  <resources>
    <!-- Texture image resource -->
    <m:texture2d id="2" path="/3D/Textures/texture.png" contenttype="image/png"/>
    
    <!-- Texture UV mapping (per-mesh) -->
    <m:texture2dgroup id="3" texid="2">
      <m:tex2coord u="0.0" v="0.0"/>
      <m:tex2coord u="1.0" v="0.0"/>
      <m:tex2coord u="1.0" v="1.0"/>
      <m:tex2coord u="0.0" v="1.0"/>
    </m:texture2dgroup>
    
    <!-- Object with texture reference -->
    <object id="4" pid="3" pindex="0">
      <mesh>
        <vertices>
          <!-- vertex positions -->
        </vertices>
        <triangles>
          <triangle v1="0" v2="1" v3="2" p1="0" p2="1" p3="2"/>
          <!-- p1, p2, p3 are indices into the texture2dgroup -->
        </triangles>
      </mesh>
    </object>
  </resources>
  <build>
    <item objectid="4"/>
  </build>
</model>
```

## Design Decisions

### 1. Per-Mesh texture2dgroups
Each mesh gets its own texture2dgroup resource, even if multiple meshes share the same material. This approach:
- ✅ Correctly handles meshes with different UV layouts but the same material
- ✅ Simpler to implement and debug
- ❌ Less efficient storage (could be optimized in the future)

### 2. Single Texture Per Material
Only the first image texture node in a material is exported. This covers the most common use case (base color texture) and avoids complexity of:
- Multiple texture channels (diffuse, normal, metallic, etc.)
- Multi-texture materials
- Complex material node setups

### 3. UV Coordinate Precision
UV coordinates are rounded to 6 decimal places to:
- Avoid floating-point comparison issues
- Reduce file size
- Maintain sufficient precision for most use cases

## Testing Recommendations

To test the texture export functionality:

1. **Simple Textured Cube**
   - Create a UV-unwrapped cube
   - Add a material with an image texture
   - Export to 3MF
   - Verify texture appears in archive

2. **Multiple Objects**
   - Create multiple objects with the same texture
   - Verify texture is shared (single texture2d)
   - Verify each mesh has its own texture2dgroup

3. **Packed vs External Textures**
   - Test with packed images
   - Test with external image files
   - Verify both export correctly

4. **Missing Textures**
   - Test with missing external files
   - Verify graceful fallback to color-only export
   - Check log for warnings

5. **No UV Maps**
   - Test object with texture but no UV map
   - Verify fallback to color-only export

## Limitations

1. **Single Texture Support**: Only exports base color texture
2. **No Normal Maps**: Additional texture channels not supported
3. **UV Layer**: Only uses active UV layer
4. **Generated Textures**: Procedural/generated textures without image source are not exported

## Future Enhancements

1. Support for multiple texture types (normal, roughness, metallic)
2. Import support for textures
3. Optimization to share texture2dgroups across meshes
4. Support for multiple UV layers
5. Better handling of complex shader node setups

## Compatibility

This implementation follows the 3MF Materials and Properties Extension specification:
- Namespace: `http://schemas.microsoft.com/3dmanufacturing/material/2015/02`
- Compatible with 3MF viewers that support the materials extension
- Gracefully degrades in viewers without texture support (shows colors only)
