'''OpenGL extension APPLE.vertex_array_object

Overview (from the spec)
	
	This extension introduces named vertex array objects which encapsulate
	vertex array state on the client side. The main purpose of these 
	objects is to keep pointers to static vertex data and provide a name 
	for different sets of static vertex data.  
	
	By extending vertex array range functionality this extension allows multiple
	vertex array ranges to exist at one time, including their complete sets of
	state, in manner analogous to texture objects. 
	
	GenVertexArraysAPPLE creates a list of n number of vertex array object
	names.  After creating a name, BindVertexArrayAPPLE associates the name with
	a vertex array object and selects this vertex array and it's associated
	state as current.  To get back to the default vertex array and its
	associated state the client should bind to vertex array named 0.
	
	Once a client is done using a vertex array object it can be deleted with
	DeleteVertexArraysAPPLE.  The client is responsible for allocating and
	deallocating the memory used by the vertex array data, while the
	DeleteVertexArraysAPPLE command deletes vertex array object names and
	associated state only.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/APPLE/vertex_array_object.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_VERTEX_ARRAY_BINDING_APPLE = constant.Constant( 'GL_VERTEX_ARRAY_BINDING_APPLE', 0x85B5 )
glBindVertexArrayAPPLE = platform.createExtensionFunction( 
	'glBindVertexArrayAPPLE', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint,),
	doc = 'glBindVertexArrayAPPLE( GLuint(array) ) -> None',
	argNames = ('array',),
)

glDeleteVertexArraysAPPLE = platform.createExtensionFunction( 
	'glDeleteVertexArraysAPPLE', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glDeleteVertexArraysAPPLE( GLsizei(n), GLuintArray(arrays) ) -> None',
	argNames = ('n', 'arrays',),
)

glGenVertexArraysAPPLE = platform.createExtensionFunction( 
	'glGenVertexArraysAPPLE', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glGenVertexArraysAPPLE( GLsizei(n), GLuintArray(arrays) ) -> None',
	argNames = ('n', 'arrays',),
)

glIsVertexArrayAPPLE = platform.createExtensionFunction( 
	'glIsVertexArrayAPPLE', dll=platform.GL,
	resultType=constants.GLboolean, 
	argTypes=(constants.GLuint,),
	doc = 'glIsVertexArrayAPPLE( GLuint(array) ) -> constants.GLboolean',
	argNames = ('array',),
)


def glInitVertexArrayObjectAPPLE():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_APPLE_vertex_array_object' )
