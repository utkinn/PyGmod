from distutils.core import setup, Extension, Command
from Cython.Build import cythonize, build_ext
# from distutils.msvccompiler import MSVCCompiler


# Garry's Mod root directory
# GMOD_DIR = 'C:\\Program Files\\Steam (x86)\\SteamApps\\Common\\GarrysMod\\garrysmod\\'


# class build_binmodule(Command):
#     def run(self):


extensions = [
    Extension(name='gmod.luastack',
              sources=['gmod/luastack.pyx'],
              language='c++'),
    Extension(name='gmod.streams',
              sources=['gmod/streams.pyx'],
              language='c++'),
]

setup(name='GPython',
      version='0.3.0-alpha',
      ext_modules=cythonize(extensions),
      cmdclass={
          'build_ext': build_ext,
          # 'build_all': build_all,
          # 'build_binmodule': build_binmodule
      })
