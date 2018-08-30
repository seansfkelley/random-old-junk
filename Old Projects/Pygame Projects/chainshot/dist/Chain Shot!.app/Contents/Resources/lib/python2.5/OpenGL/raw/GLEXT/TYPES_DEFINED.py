'''OpenGL extension .TYPES_DEFINED

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry//TYPES_DEFINED.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes



def glInitTypesDefined():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GLEXT__TYPES_DEFINED' )
