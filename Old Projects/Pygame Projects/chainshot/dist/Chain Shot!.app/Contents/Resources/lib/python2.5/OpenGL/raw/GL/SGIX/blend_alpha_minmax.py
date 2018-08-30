'''OpenGL extension SGIX.blend_alpha_minmax

Overview (from the spec)
	
	Two additional blending equations are specified using the interface
	defined by EXT_blend_minmax.  These equations are similar to the
	MIN_EXT and MAX_EXT blending equations, but the outcome for all four
	color components is determined by a comparison of just the alpha
	component's source and destination values.  These equations are useful
	in image processing and advanced shading algorithms.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SGIX/blend_alpha_minmax.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_ALPHA_MIN_SGIX = constant.Constant( 'GL_ALPHA_MIN_SGIX', 0x8320 )
GL_ALPHA_MAX_SGIX = constant.Constant( 'GL_ALPHA_MAX_SGIX', 0x8321 )


def glInitBlendAlphaMinmaxSGIX():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SGIX_blend_alpha_minmax' )