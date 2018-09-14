# GPython
Experimental project which strives to provide the possibility to create addons for Garry's Mod
with Python 3 programming language.

## Requirements for building
1. Cython
2. Visual Studio 2017

## Building
1. Copy `lua_launcher\gpython_launcher` directory to `garrysmod\addons` directory.
1. Open command prompt, `cd` to `python_extensions` directory and run `setup.py build_ext --inplace`.
4. Move all files with `.pyd` extension in `python_extensions` directory to `garrysmod\gpython` directory and
in `python_extensions\gmod` to `garrysmod\gpython\gmod` (create them if they doesn't exist).
2. Open `GPython.sln` with Visual Studio and build the solution.
3. Move `gmsv_gpython_win32.dll` and `gmcl_gpython_win32.dll`
from `bin_modules\build` directory to `garrysmod\lua\bin` directory.
4. Move `gpython.dll` to Garry's Mod's root directory (where `hl2.exe` resides).
