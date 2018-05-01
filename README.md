Vulcano File Format (.vmsh) Exporter
====
In order for Blender to be able to find the add-on:
1. Create a base directory e.g. "BlenderScripts".
2. In **Blender -> User Preferences -> File -> Scripts** set the path to point to the base directory that contains the scripts, e.g. "Blender".
3. Create a directory ["addons"][1].
4. If the addon is structured as a Python package in a subdirectory:
   * *On Windows:* Create directory junction with  [`mklink /J link target`][2].
   * *On Linux:* Create a symlink to the Python package folder.
5. It may be necessary to enable the add-on in **Blender -> User Preferences -> Add-ons**.
6. *Optional:* Create a `.blend` as a workspace file to use the built-in Text Editor and link the corresponding Python source files from the add-on Python package.

[1]: https://docs.blender.org/manual/en/dev/preferences/file.html#scripts-path
[2]: https://ss64.com/nt/mklink.html

Files
----
* MakeDirectoryJunction.bat - Creates the required symlink on Windows
* VulcanoExporter.blend - Blender project file

Notes
----
If the Python files are edited with an external editor they need to be reloaded from inside of Blender with *"Text -> Reload (Ctrl-R)"*.
