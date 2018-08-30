'''OpenGL extension ARB.half_float_pixel

Overview (from the spec)
	
	This extension introduces a new data type for half-precision (16-bit)
	floating-point quantities.  The floating-point format is very similar
	to the IEEE single-precision floating-point standard, except that it
	has only 5 exponent bits and 10 mantissa bits.  Half-precision floats
	are smaller than full precision floats and provide a larger dynamic
	range than similarly sized normalized scalar data types.
	
	This extension allows applications to use half-precision floating-
	point data when specifying pixel data.  It extends the existing image
	specification commands to accept the new data type.
	
	Floating-point data is clamped to [0, 1] at various places in the
	GL unless clamping is disabled with the ARB_color_buffer_float
	extension.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/ARB/half_float_pixel.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_HALF_FLOAT_ARB = constant.Constant( 'GL_HALF_FLOAT_ARB', 0x140B )


def glInitHalfFloatPixelARB():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_ARB_half_float_pixel' )
