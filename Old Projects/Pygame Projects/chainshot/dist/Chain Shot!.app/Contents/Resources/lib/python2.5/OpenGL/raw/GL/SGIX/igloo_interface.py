'''OpenGL extension SGIX.igloo_interface

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SGIX/igloo_interface.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes

glIglooInterfaceSGIX = platform.createExtensionFunction( 
	'glIglooInterfaceSGIX', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, ctypes.c_void_p,),
	doc = 'glIglooInterfaceSGIX( GLenum(pname), c_void_p(params) ) -> None',
	argNames = ('pname', 'params',),
)


def glInitIglooInterfaceSGIX():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SGIX_igloo_interface' )
