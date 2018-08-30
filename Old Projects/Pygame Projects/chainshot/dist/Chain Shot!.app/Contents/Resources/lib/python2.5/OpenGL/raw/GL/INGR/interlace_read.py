'''OpenGL extension INGR.interlace_read

Overview (from the spec)
	
	This extension provides a way to skip rows of pixels when reading
	or copying pixel rectangles.  This extension is complementary to
	the EXT_interlace extension except that it has no affect on getting
	texture images.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/INGR/interlace_read.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_INTERLACE_READ_INGR = constant.Constant( 'GL_INTERLACE_READ_INGR', 0x8568 )
glget.addGLGetConstant( GL_INTERLACE_READ_INGR, (1,) )


def glInitInterlaceReadINGR():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_INGR_interlace_read' )