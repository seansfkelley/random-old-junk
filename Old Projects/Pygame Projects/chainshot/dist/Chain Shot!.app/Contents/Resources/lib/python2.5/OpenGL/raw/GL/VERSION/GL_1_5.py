'''OpenGL extension VERSION.GL_1_5

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/VERSION/GL_1_5.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_BUFFER_SIZE = constant.Constant( 'GL_BUFFER_SIZE', 0x8764 )
GL_BUFFER_USAGE = constant.Constant( 'GL_BUFFER_USAGE', 0x8765 )
GL_QUERY_COUNTER_BITS = constant.Constant( 'GL_QUERY_COUNTER_BITS', 0x8864 )
GL_CURRENT_QUERY = constant.Constant( 'GL_CURRENT_QUERY', 0x8865 )
GL_QUERY_RESULT = constant.Constant( 'GL_QUERY_RESULT', 0x8866 )
GL_QUERY_RESULT_AVAILABLE = constant.Constant( 'GL_QUERY_RESULT_AVAILABLE', 0x8867 )
GL_ARRAY_BUFFER = constant.Constant( 'GL_ARRAY_BUFFER', 0x8892 )
GL_ELEMENT_ARRAY_BUFFER = constant.Constant( 'GL_ELEMENT_ARRAY_BUFFER', 0x8893 )
GL_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_ARRAY_BUFFER_BINDING', 0x8894 )
GL_ELEMENT_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_ELEMENT_ARRAY_BUFFER_BINDING', 0x8895 )
GL_VERTEX_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_VERTEX_ARRAY_BUFFER_BINDING', 0x8896 )
GL_NORMAL_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_NORMAL_ARRAY_BUFFER_BINDING', 0x8897 )
GL_COLOR_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_COLOR_ARRAY_BUFFER_BINDING', 0x8898 )
GL_INDEX_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_INDEX_ARRAY_BUFFER_BINDING', 0x8899 )
GL_TEXTURE_COORD_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_TEXTURE_COORD_ARRAY_BUFFER_BINDING', 0x889A )
GL_EDGE_FLAG_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_EDGE_FLAG_ARRAY_BUFFER_BINDING', 0x889B )
GL_SECONDARY_COLOR_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_SECONDARY_COLOR_ARRAY_BUFFER_BINDING', 0x889C )
GL_FOG_COORDINATE_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_FOG_COORDINATE_ARRAY_BUFFER_BINDING', 0x889D )
GL_WEIGHT_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_WEIGHT_ARRAY_BUFFER_BINDING', 0x889E )
GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING', 0x889F )
GL_READ_ONLY = constant.Constant( 'GL_READ_ONLY', 0x88B8 )
GL_WRITE_ONLY = constant.Constant( 'GL_WRITE_ONLY', 0x88B9 )
GL_READ_WRITE = constant.Constant( 'GL_READ_WRITE', 0x88BA )
GL_BUFFER_ACCESS = constant.Constant( 'GL_BUFFER_ACCESS', 0x88BB )
GL_BUFFER_MAPPED = constant.Constant( 'GL_BUFFER_MAPPED', 0x88BC )
GL_BUFFER_MAP_POINTER = constant.Constant( 'GL_BUFFER_MAP_POINTER', 0x88BD )
GL_STREAM_DRAW = constant.Constant( 'GL_STREAM_DRAW', 0x88E0 )
GL_STREAM_READ = constant.Constant( 'GL_STREAM_READ', 0x88E1 )
GL_STREAM_COPY = constant.Constant( 'GL_STREAM_COPY', 0x88E2 )
GL_STATIC_DRAW = constant.Constant( 'GL_STATIC_DRAW', 0x88E4 )
GL_STATIC_READ = constant.Constant( 'GL_STATIC_READ', 0x88E5 )
GL_STATIC_COPY = constant.Constant( 'GL_STATIC_COPY', 0x88E6 )
GL_DYNAMIC_DRAW = constant.Constant( 'GL_DYNAMIC_DRAW', 0x88E8 )
GL_DYNAMIC_READ = constant.Constant( 'GL_DYNAMIC_READ', 0x88E9 )
GL_DYNAMIC_COPY = constant.Constant( 'GL_DYNAMIC_COPY', 0x88EA )
GL_SAMPLES_PASSED = constant.Constant( 'GL_SAMPLES_PASSED', 0x8914 )
glGenQueries = platform.createExtensionFunction( 
	'glGenQueries', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glGenQueries( GLsizei(n), GLuintArray(ids) ) -> None',
	argNames = ('n', 'ids',),
)

glDeleteQueries = platform.createExtensionFunction( 
	'glDeleteQueries', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glDeleteQueries( GLsizei(n), GLuintArray(ids) ) -> None',
	argNames = ('n', 'ids',),
)

glIsQuery = platform.createExtensionFunction( 
	'glIsQuery', dll=platform.GL,
	resultType=constants.GLboolean, 
	argTypes=(constants.GLuint,),
	doc = 'glIsQuery( GLuint(id) ) -> constants.GLboolean',
	argNames = ('id',),
)

glBeginQuery = platform.createExtensionFunction( 
	'glBeginQuery', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLuint,),
	doc = 'glBeginQuery( GLenum(target), GLuint(id) ) -> None',
	argNames = ('target', 'id',),
)

glEndQuery = platform.createExtensionFunction( 
	'glEndQuery', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum,),
	doc = 'glEndQuery( GLenum(target) ) -> None',
	argNames = ('target',),
)

glGetQueryiv = platform.createExtensionFunction( 
	'glGetQueryiv', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLenum, arrays.GLintArray,),
	doc = 'glGetQueryiv( GLenum(target), GLenum(pname), GLintArray(params) ) -> None',
	argNames = ('target', 'pname', 'params',),
)

glGetQueryObjectiv = platform.createExtensionFunction( 
	'glGetQueryObjectiv', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLenum, arrays.GLintArray,),
	doc = 'glGetQueryObjectiv( GLuint(id), GLenum(pname), GLintArray(params) ) -> None',
	argNames = ('id', 'pname', 'params',),
)

glGetQueryObjectuiv = platform.createExtensionFunction( 
	'glGetQueryObjectuiv', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLenum, arrays.GLuintArray,),
	doc = 'glGetQueryObjectuiv( GLuint(id), GLenum(pname), GLuintArray(params) ) -> None',
	argNames = ('id', 'pname', 'params',),
)

glBindBuffer = platform.createExtensionFunction( 
	'glBindBuffer', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLuint,),
	doc = 'glBindBuffer( GLenum(target), GLuint(buffer) ) -> None',
	argNames = ('target', 'buffer',),
)

glDeleteBuffers = platform.createExtensionFunction( 
	'glDeleteBuffers', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glDeleteBuffers( GLsizei(n), GLuintArray(buffers) ) -> None',
	argNames = ('n', 'buffers',),
)

glGenBuffers = platform.createExtensionFunction( 
	'glGenBuffers', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glGenBuffers( GLsizei(n), GLuintArray(buffers) ) -> None',
	argNames = ('n', 'buffers',),
)

glIsBuffer = platform.createExtensionFunction( 
	'glIsBuffer', dll=platform.GL,
	resultType=constants.GLboolean, 
	argTypes=(constants.GLuint,),
	doc = 'glIsBuffer( GLuint(buffer) ) -> constants.GLboolean',
	argNames = ('buffer',),
)

glBufferData = platform.createExtensionFunction( 
	'glBufferData', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLsizeiptr, ctypes.c_void_p, constants.GLenum,),
	doc = 'glBufferData( GLenum(target), GLsizeiptr(size), c_void_p(data), GLenum(usage) ) -> None',
	argNames = ('target', 'size', 'data', 'usage',),
)

glBufferSubData = platform.createExtensionFunction( 
	'glBufferSubData', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLintptr, constants.GLsizeiptr, ctypes.c_void_p,),
	doc = 'glBufferSubData( GLenum(target), GLintptr(offset), GLsizeiptr(size), c_void_p(data) ) -> None',
	argNames = ('target', 'offset', 'size', 'data',),
)

glGetBufferSubData = platform.createExtensionFunction( 
	'glGetBufferSubData', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLintptr, constants.GLsizeiptr, ctypes.c_void_p,),
	doc = 'glGetBufferSubData( GLenum(target), GLintptr(offset), GLsizeiptr(size), c_void_p(data) ) -> None',
	argNames = ('target', 'offset', 'size', 'data',),
)

glMapBuffer = platform.createExtensionFunction( 
	'glMapBuffer', dll=platform.GL,
	resultType=ctypes.c_void_p, 
	argTypes=(constants.GLenum, constants.GLenum,),
	doc = 'glMapBuffer( GLenum(target), GLenum(access) ) -> ctypes.c_void_p',
	argNames = ('target', 'access',),
)

glUnmapBuffer = platform.createExtensionFunction( 
	'glUnmapBuffer', dll=platform.GL,
	resultType=constants.GLboolean, 
	argTypes=(constants.GLenum,),
	doc = 'glUnmapBuffer( GLenum(target) ) -> constants.GLboolean',
	argNames = ('target',),
)

glGetBufferParameteriv = platform.createExtensionFunction( 
	'glGetBufferParameteriv', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLenum, arrays.GLintArray,),
	doc = 'glGetBufferParameteriv( GLenum(target), GLenum(pname), GLintArray(params) ) -> None',
	argNames = ('target', 'pname', 'params',),
)

glGetBufferPointerv = platform.createExtensionFunction( 
	'glGetBufferPointerv', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLenum, ctypes.POINTER(ctypes.c_void_p),),
	doc = 'glGetBufferPointerv( GLenum(target), GLenum(pname), POINTER(ctypes.c_void_p)(params) ) -> None',
	argNames = ('target', 'pname', 'params',),
)
