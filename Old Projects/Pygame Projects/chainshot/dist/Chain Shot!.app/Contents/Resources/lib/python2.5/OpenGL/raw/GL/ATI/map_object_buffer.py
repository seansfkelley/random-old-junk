'''OpenGL extension ATI.map_object_buffer

Overview (from the spec)
	
	This extension provides a mechanism for an application to obtain
	the virtual address of an object buffer. This allows the
	application to directly update the contents of an object buffer
	and avoid any intermediate copies.
	

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/ATI/map_object_buffer.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes

glMapObjectBufferATI = platform.createExtensionFunction( 
	'glMapObjectBufferATI', dll=platform.GL,
	resultType=ctypes.c_void_p, 
	argTypes=(constants.GLuint,),
	doc = 'glMapObjectBufferATI( GLuint(buffer) ) -> ctypes.c_void_p',
	argNames = ('buffer',),
)

glUnmapObjectBufferATI = platform.createExtensionFunction( 
	'glUnmapObjectBufferATI', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint,),
	doc = 'glUnmapObjectBufferATI( GLuint(buffer) ) -> None',
	argNames = ('buffer',),
)


def glInitMapObjectBufferATI():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_ATI_map_object_buffer' )