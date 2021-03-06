'''OpenGL extension SUN.convolution_border_modes

Overview (from the spec)
	
	This extension provides an additional border mode for the
	EXT_convolution extension.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SUN/convolution_border_modes.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_WRAP_BORDER_SUN = constant.Constant( 'GL_WRAP_BORDER_SUN', 0x81D4 )


def glInitConvolutionBorderModesSUN():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SUN_convolution_border_modes' )
