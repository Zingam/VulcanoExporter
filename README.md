Vulcano File Format (.vmsh)
====

Description
----
[<img src="https://download.blender.org/institute/logos/blender-plain.png" width=200>][1]

[**Blender**][1] based 3D data exporter

Requirements
----
* [**Blender 2.79**][1]

[1]: https://www.blender.org

How to Develop with Blender
----
In order for Blender to be able to find the add-on:
1. Create a base directory e.g. "BlenderScripts".
2. In **Blender -> User Preferences -> File -> Scripts** set the path to point to the base directory that contains the scripts, e.g. "Blender".
3. Create a directory ["addons"][2].
4. If the addon is structured as a Python package in a subdirectory:
   * *On Windows:* Create *a directory junction* with  [`mklink /j <link> <target>`][3].
   * *On Linux:* Create *a symlink* to the Python package folder.
5. It may be necessary to enable the add-on in **Blender -> User Preferences -> Add-ons**.
6. *Optional:* Create a `*.blend` file in Blender as a workspace file to use the built-in Text Editor and link the corresponding Python source files from the add-on Python package.

[2]: https://docs.blender.org/manual/en/dev/preferences/file.html#scripts-path
[3]: https://ss64.com/nt/mklink.html

Files
----
* MakeSymlink.bat - Creates the required symbolic link on Windows

Notes
----
If a `*.blend` file is used as *a workspace file* and in case the Python files are edited with an external editor they need to be reloaded from inside of Blender with **Text -> Reload (Ctrl-R)** every time. Otherwise the externally edited file might be overwritten by a different version of the file linked to *the* `*.blend` *workspace file*.
