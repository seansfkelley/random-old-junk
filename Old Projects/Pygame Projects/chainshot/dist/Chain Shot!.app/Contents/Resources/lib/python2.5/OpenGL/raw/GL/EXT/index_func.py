'''OpenGL extension EXT.index_func

Overview (from the spec)
	
	This extension provides a way to discard fragments when a comparison
	between the fragment's index value and a reference index fails.  This
	may be used similarly to the alpha test which is available in RGBA mode.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/EXT/index_func.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_INDEX_TEST_EXT = constant.Constant( 'GL_INDEX_TEST_EXT', 0x81B5 )
GL_INDEX_TEST_FUNC_EXT = constant.Constant( 'GL_INDEX_TEST_FUNC_EXT', 0x81B6 )
GL_INDEX_TEST_REF_EXT = constant.Constant( 'GL_INDEX_TEST_REF_EXT', 0x81B7 )
glIndexFuncEXT = platform.createExtensionFunction( 
	'glIndexFuncEXT', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLclampf,),
	doc = 'glIndexFuncEXT( GLenum(func), GLclampf(ref) ) -> None',
	argNames = ('func', 'ref',),
)


def glInitIndexFuncEXT():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_EXT_index_func' )
