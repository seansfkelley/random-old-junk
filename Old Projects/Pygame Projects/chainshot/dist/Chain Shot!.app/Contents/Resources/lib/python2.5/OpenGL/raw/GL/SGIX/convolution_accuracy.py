'''OpenGL extension SGIX.convolution_accuracy

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SGIX/convolution_accuracy.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_CONVOLUTION_HINT_SGIX = constant.Constant( 'GL_CONVOLUTION_HINT_SGIX', 0x8316 )


def glInitConvolutionAccuracySGIX():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SGIX_convolution_accuracy' )
