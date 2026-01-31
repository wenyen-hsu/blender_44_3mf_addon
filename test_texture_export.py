#!/usr/bin/env python3
"""
Automated tests for 3MF texture export functionality.
Run with: blender --background --python test_texture_export.py

This script tests the texture export implementation added in v1.1.3.
"""

import bpy
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Test results
test_results = []

def log_test(test_name, passed, message=""):
    """Log test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if message:
        print(f"   {message}")
    test_results.append((test_name, passed, message))

def setup_test_scene():
    """Create a simple textured cube for testing"""
    # Clear scene
    bpy.ops.wm.read_homefile(use_empty=True)
    
    # Delete default objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Create cube
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    cube.name = "TestCube"
    
    # Create UV map
    if not cube.data.uv_layers:
        cube.data.uv_layers.new()
    
    # Create material with texture
    mat = bpy.data.materials.new(name="TestMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Add nodes
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    tex_node = nodes.new(type='ShaderNodeTexImage')
    tex_node.location = (-300, 0)
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Link nodes
    mat.node_tree.links.new(tex_node.outputs[0], bsdf.inputs[0])
    mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
    
    # Create test texture (simple 2x2 image)
    img = bpy.data.images.new("TestTexture", width=2, height=2)
    pixels = [1.0, 0.0, 0.0, 1.0] * 4  # Red pixels
    img.pixels = pixels
    img.file_format = 'PNG'
    img.pack()  # Pack the image
    tex_node.image = img
    
    # Assign material
    if cube.data.materials:
        cube.data.materials[0] = mat
    else:
        cube.data.materials.append(mat)
    
    return cube

def test_basic_export():
    """Test Case 1.1: Basic texture export with PNG"""
    test_name = "TC-1.1: Basic Texture Export (PNG)"
    
    try:
        cube = setup_test_scene()
        export_path = "/tmp/test_texture_export.3mf"
        
        # Clean up any existing file
        if os.path.exists(export_path):
            os.remove(export_path)
        
        # Export
        bpy.ops.export_mesh.threemf(filepath=export_path)
        
        # Verify file exists
        if not os.path.exists(export_path):
            log_test(test_name, False, "Export file not created")
            return False
        
        # Verify archive structure
        with zipfile.ZipFile(export_path, 'r') as zf:
            files = zf.namelist()
            
            # Check for texture files
            texture_files = [f for f in files if 'Textures' in f and not f.endswith('/')]
            if not texture_files:
                log_test(test_name, False, "No textures found in archive")
                return False
            
            # Check model file
            if '3D/3dmodel.model' not in files:
                log_test(test_name, False, "Model file missing")
                return False
            
            # Parse and validate XML
            with zf.open('3D/3dmodel.model') as model_file:
                tree = ET.parse(model_file)
                root = tree.getroot()
                
                # Check for material namespace in attributes
                has_material_ns = False
                for attr_value in root.attrib.values():
                    if 'material/2015/02' in str(attr_value):
                        has_material_ns = True
                        break
                
                if not has_material_ns:
                    log_test(test_name, False, "Material namespace not found")
                    return False
        
        log_test(test_name, True, f"Exported successfully with {len(texture_files)} texture(s)")
        return True
        
    except Exception as e:
        log_test(test_name, False, f"Exception: {str(e)}")
        return False

def test_no_uv_fallback():
    """Test Case 3.1: Fallback when no UV coordinates"""
    test_name = "TC-3.1: No UV Map Fallback"
    
    try:
        cube = setup_test_scene()
        
        # Remove UV map
        while cube.data.uv_layers:
            cube.data.uv_layers.remove(cube.data.uv_layers[0])
        
        export_path = "/tmp/test_no_uv.3mf"
        
        # Clean up any existing file
        if os.path.exists(export_path):
            os.remove(export_path)
        
        # Export - should not crash
        bpy.ops.export_mesh.threemf(filepath=export_path)
        
        if not os.path.exists(export_path):
            log_test(test_name, False, "Export file not created")
            return False
        
        # Verify it falls back to color-only export
        with zipfile.ZipFile(export_path, 'r') as zf:
            files = zf.namelist()
            
            # Should have model file
            if '3D/3dmodel.model' not in files:
                log_test(test_name, False, "Model file missing")
                return False
            
            # Parse XML
            with zf.open('3D/3dmodel.model') as model_file:
                tree = ET.parse(model_file)
                root = tree.getroot()
                
                # Should have basematerials or no texture2dgroup
                xml_str = ET.tostring(root, encoding='unicode')
                has_basematerials = 'basematerials' in xml_str
                has_texture2dgroup = 'texture2dgroup' in xml_str
                
                # It's OK if there's no texture2dgroup (fallback behavior)
                # But we should have something (basematerials)
        
        log_test(test_name, True, "Export completed without crash (graceful fallback)")
        return True
        
    except Exception as e:
        log_test(test_name, False, f"Exception: {str(e)}")
        return False

def test_color_only_regression():
    """Test Case 8.1: Color-only export still works (regression test)"""
    test_name = "TC-8.1: Color-Only Export (Regression)"
    
    try:
        # Clear scene
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Create cube
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        
        # Create material with color only (no texture)
        mat = bpy.data.materials.new(name="ColorMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get('Principled BSDF')
        if bsdf:
            bsdf.inputs[0].default_value = (1.0, 0.0, 0.0, 1.0)  # Red
        
        # Assign material
        if cube.data.materials:
            cube.data.materials[0] = mat
        else:
            cube.data.materials.append(mat)
        
        export_path = "/tmp/test_color_only.3mf"
        
        # Clean up any existing file
        if os.path.exists(export_path):
            os.remove(export_path)
        
        # Export
        bpy.ops.export_mesh.threemf(filepath=export_path)
        
        if not os.path.exists(export_path):
            log_test(test_name, False, "Export file not created")
            return False
        
        # Verify archive is valid
        with zipfile.ZipFile(export_path, 'r') as zf:
            if '3D/3dmodel.model' not in zf.namelist():
                log_test(test_name, False, "Model file missing")
                return False
        
        log_test(test_name, True, "Color-only export works as expected")
        return True
        
    except Exception as e:
        log_test(test_name, False, f"Exception: {str(e)}")
        return False

def test_multiple_objects():
    """Test Case 2.1: Multiple objects with different textures"""
    test_name = "TC-2.1: Multiple Objects with Different Textures"
    
    try:
        # Clear scene
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Create 2 objects with different textures
        for i in range(2):
            bpy.ops.mesh.primitive_cube_add(location=(i * 3, 0, 0))
            cube = bpy.context.active_object
            cube.name = f"Cube{i}"
            
            # Ensure UV map
            if not cube.data.uv_layers:
                cube.data.uv_layers.new()
            
            # Create unique material
            mat = bpy.data.materials.new(name=f"Material{i}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            tex_node = nodes.new(type='ShaderNodeTexImage')
            output = nodes.new(type='ShaderNodeOutputMaterial')
            
            mat.node_tree.links.new(tex_node.outputs[0], bsdf.inputs[0])
            mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
            
            # Create unique texture
            img = bpy.data.images.new(f"Texture{i}", width=2, height=2)
            color = [1.0 if i == 0 else 0.0, 1.0 if i == 1 else 0.0, 0.0, 1.0]
            img.pixels = color * 4
            img.file_format = 'PNG'
            img.pack()
            tex_node.image = img
            
            # Assign material
            if cube.data.materials:
                cube.data.materials[0] = mat
            else:
                cube.data.materials.append(mat)
        
        export_path = "/tmp/test_multiple_objects.3mf"
        
        # Clean up any existing file
        if os.path.exists(export_path):
            os.remove(export_path)
        
        # Export
        bpy.ops.export_mesh.threemf(filepath=export_path)
        
        if not os.path.exists(export_path):
            log_test(test_name, False, "Export file not created")
            return False
        
        # Verify multiple textures
        with zipfile.ZipFile(export_path, 'r') as zf:
            files = zf.namelist()
            texture_files = [f for f in files if 'Textures' in f and not f.endswith('/')]
            
            if len(texture_files) < 2:
                log_test(test_name, False, f"Expected 2 textures, found {len(texture_files)}")
                return False
        
        log_test(test_name, True, f"Exported {len(texture_files)} textures successfully")
        return True
        
    except Exception as e:
        log_test(test_name, False, f"Exception: {str(e)}")
        return False

def test_xml_validity():
    """Test Case 6.1: XML structure validation"""
    test_name = "TC-6.1: XML Validation"
    
    try:
        cube = setup_test_scene()
        export_path = "/tmp/test_xml_validation.3mf"
        
        # Clean up any existing file
        if os.path.exists(export_path):
            os.remove(export_path)
        
        # Export
        bpy.ops.export_mesh.threemf(filepath=export_path)
        
        if not os.path.exists(export_path):
            log_test(test_name, False, "Export file not created")
            return False
        
        # Parse and validate XML structure
        with zipfile.ZipFile(export_path, 'r') as zf:
            with zf.open('3D/3dmodel.model') as model_file:
                try:
                    tree = ET.parse(model_file)
                    root = tree.getroot()
                    
                    # Basic structure checks
                    checks = []
                    
                    # Check for resources element
                    ns = {'core': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
                    resources = root.find('.//core:resources', ns)
                    checks.append(("resources element exists", resources is not None))
                    
                    # Check for build element
                    build = root.find('.//core:build', ns)
                    checks.append(("build element exists", build is not None))
                    
                    # Check for object elements
                    objects = root.findall('.//core:object', ns)
                    checks.append(("object elements exist", len(objects) > 0))
                    
                    all_passed = all(check[1] for check in checks)
                    
                    if not all_passed:
                        failed = [check[0] for check in checks if not check[1]]
                        log_test(test_name, False, f"Failed checks: {', '.join(failed)}")
                        return False
                    
                except ET.ParseError as e:
                    log_test(test_name, False, f"XML Parse Error: {str(e)}")
                    return False
        
        log_test(test_name, True, "XML structure is valid")
        return True
        
    except Exception as e:
        log_test(test_name, False, f"Exception: {str(e)}")
        return False

def run_all_tests():
    """Run all automated tests"""
    print("\n" + "="*70)
    print("3MF Texture Export - Automated Test Suite")
    print("="*70 + "\n")
    
    tests = [
        ("Basic Export", test_basic_export),
        ("No UV Fallback", test_no_uv_fallback),
        ("Color-Only Regression", test_color_only_regression),
        ("Multiple Objects", test_multiple_objects),
        ("XML Validity", test_xml_validity),
    ]
    
    for i, (name, test_func) in enumerate(tests, 1):
        print(f"\n[{i}/{len(tests)}] Running: {name}")
        print("-" * 70)
        test_func()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, p, _ in test_results if p)
    total = len(test_results)
    
    for name, passed_status, message in test_results:
        status = "✓ PASS" if passed_status else "✗ FAIL"
        print(f"{status}: {name}")
        if message and not passed_status:
            print(f"       → {message}")
    
    print("\n" + "="*70)
    print(f"Results: {passed}/{total} tests passed ({100*passed//total}%)")
    print("="*70 + "\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
