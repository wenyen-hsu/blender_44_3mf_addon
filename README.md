# Blender 3MF Import/Export Add-on

This add-on allows Blender to import and export 3MF files, a format used for 3D printing applications.

## Features

- Import and export 3MF files to and from Blender
- Supports materials and metadata
- Compatible with Blender 2.80 through 4.4+
- Handles meshes, colors, and transformations

## Installation

1. Download the add-on as a ZIP file
2. In Blender, go to Edit > Preferences
3. Select the "Add-ons" tab
4. Click "Install..." and select the downloaded ZIP file
5. Enable the add-on by checking the box next to "Import-Export: 3MF format"

## Usage

### Importing 3MF Files

1. Go to File > Import > 3D Manufacturing Format (.3mf)
2. Select the 3MF file to import
3. Adjust import settings as needed
4. Click "Import 3MF"

### Exporting 3MF Files

1. Go to File > Export > 3D Manufacturing Format (.3mf)
2. Select the file location and name
3. Adjust export settings such as scale, selection only, etc.
4. Click "Export 3MF"

## Compatibility

This add-on has been updated to be compatible with Blender 4.4+. It addresses the following API changes:

- Updated initialization of operator classes to properly pass arguments to parent classes
- Support for Blender 3.2+ view context handling
- Fixed metadata handling to prevent TypeError when metadata contains None values (v1.1.0)

### Bugfixes

#### v1.1.0
- Fixed an issue where importing 3MF files would fail with `TypeError: bpy_struct: item.attr = val: Scene.name doesn't support None from string types` by adding a null check before setting object names from metadata

## License

This add-on is released under the GNU General Public License version 2.0 or later.

## Credits

Original author: Ghostkeeper  
Updated for Blender 4.4 compatibility
