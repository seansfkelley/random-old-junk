'''OpenGL extension ARB.imaging

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.imaging to provide a more 
Python-friendly API
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.ARB.imaging import *
### END AUTOGENERATED SECTION