'''OpenGL extension SUN.vertex

Overview (from the spec)
	
	This extension provides new GL commands to specify vertex data such as 
	color and normal along with the vertex in one single GL command in order to
	minimize the overhead in making GL commands for each set of vertex data.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SUN/vertex.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes

glColor4ubVertex2fSUN = platform.createExtensionFunction( 
	'glColor4ubVertex2fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLfloat, constants.GLfloat,),
	doc = 'glColor4ubVertex2fSUN( GLubyte(r), GLubyte(g), GLubyte(b), GLubyte(a), GLfloat(x), GLfloat(y) ) -> None',
	argNames = ('r', 'g', 'b', 'a', 'x', 'y',),
)

glColor4ubVertex2fvSUN = platform.createExtensionFunction( 
	'glColor4ubVertex2fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLubyteArray, arrays.GLfloatArray,),
	doc = 'glColor4ubVertex2fvSUN( GLubyteArray(c), GLfloatArray(v) ) -> None',
	argNames = ('c', 'v',),
)

glColor4ubVertex3fSUN = platform.createExtensionFunction( 
	'glColor4ubVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glColor4ubVertex3fSUN( GLubyte(r), GLubyte(g), GLubyte(b), GLubyte(a), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('r', 'g', 'b', 'a', 'x', 'y', 'z',),
)

glColor4ubVertex3fvSUN = platform.createExtensionFunction( 
	'glColor4ubVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLubyteArray, arrays.GLfloatArray,),
	doc = 'glColor4ubVertex3fvSUN( GLubyteArray(c), GLfloatArray(v) ) -> None',
	argNames = ('c', 'v',),
)

glColor3fVertex3fSUN = platform.createExtensionFunction( 
	'glColor3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glColor3fVertex3fSUN( GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('r', 'g', 'b', 'x', 'y', 'z',),
)

glColor3fVertex3fvSUN = platform.createExtensionFunction( 
	'glColor3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glColor3fVertex3fvSUN( GLfloatArray(c), GLfloatArray(v) ) -> None',
	argNames = ('c', 'v',),
)

glNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glNormal3fVertex3fSUN( GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glNormal3fVertex3fvSUN( GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('n', 'v',),
)

glColor4fNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glColor4fNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glColor4fNormal3fVertex3fSUN( GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(a), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('r', 'g', 'b', 'a', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glColor4fNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glColor4fNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glColor4fNormal3fVertex3fvSUN( GLfloatArray(c), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('c', 'n', 'v',),
)

glTexCoord2fVertex3fSUN = platform.createExtensionFunction( 
	'glTexCoord2fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord2fVertex3fSUN( GLfloat(s), GLfloat(t), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('s', 't', 'x', 'y', 'z',),
)

glTexCoord2fVertex3fvSUN = platform.createExtensionFunction( 
	'glTexCoord2fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glTexCoord2fVertex3fvSUN( GLfloatArray(tc), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'v',),
)

glTexCoord4fVertex4fSUN = platform.createExtensionFunction( 
	'glTexCoord4fVertex4fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord4fVertex4fSUN( GLfloat(s), GLfloat(t), GLfloat(p), GLfloat(q), GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w) ) -> None',
	argNames = ('s', 't', 'p', 'q', 'x', 'y', 'z', 'w',),
)

glTexCoord4fVertex4fvSUN = platform.createExtensionFunction( 
	'glTexCoord4fVertex4fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glTexCoord4fVertex4fvSUN( GLfloatArray(tc), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'v',),
)

glTexCoord2fColor4ubVertex3fSUN = platform.createExtensionFunction( 
	'glTexCoord2fColor4ubVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord2fColor4ubVertex3fSUN( GLfloat(s), GLfloat(t), GLubyte(r), GLubyte(g), GLubyte(b), GLubyte(a), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('s', 't', 'r', 'g', 'b', 'a', 'x', 'y', 'z',),
)

glTexCoord2fColor4ubVertex3fvSUN = platform.createExtensionFunction( 
	'glTexCoord2fColor4ubVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLubyteArray, arrays.GLfloatArray,),
	doc = 'glTexCoord2fColor4ubVertex3fvSUN( GLfloatArray(tc), GLubyteArray(c), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'c', 'v',),
)

glTexCoord2fColor3fVertex3fSUN = platform.createExtensionFunction( 
	'glTexCoord2fColor3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord2fColor3fVertex3fSUN( GLfloat(s), GLfloat(t), GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('s', 't', 'r', 'g', 'b', 'x', 'y', 'z',),
)

glTexCoord2fColor3fVertex3fvSUN = platform.createExtensionFunction( 
	'glTexCoord2fColor3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glTexCoord2fColor3fVertex3fvSUN( GLfloatArray(tc), GLfloatArray(c), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'c', 'v',),
)

glTexCoord2fNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glTexCoord2fNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord2fNormal3fVertex3fSUN( GLfloat(s), GLfloat(t), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('s', 't', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glTexCoord2fNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glTexCoord2fNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glTexCoord2fNormal3fVertex3fvSUN( GLfloatArray(tc), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'n', 'v',),
)

glTexCoord2fColor4fNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glTexCoord2fColor4fNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord2fColor4fNormal3fVertex3fSUN( GLfloat(s), GLfloat(t), GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(a), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('s', 't', 'r', 'g', 'b', 'a', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glTexCoord2fColor4fNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glTexCoord2fColor4fNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glTexCoord2fColor4fNormal3fVertex3fvSUN( GLfloatArray(tc), GLfloatArray(c), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'c', 'n', 'v',),
)

glTexCoord4fColor4fNormal3fVertex4fSUN = platform.createExtensionFunction( 
	'glTexCoord4fColor4fNormal3fVertex4fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glTexCoord4fColor4fNormal3fVertex4fSUN( GLfloat(s), GLfloat(t), GLfloat(p), GLfloat(q), GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(a), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w) ) -> None',
	argNames = ('s', 't', 'p', 'q', 'r', 'g', 'b', 'a', 'nx', 'ny', 'nz', 'x', 'y', 'z', 'w',),
)

glTexCoord4fColor4fNormal3fVertex4fvSUN = platform.createExtensionFunction( 
	'glTexCoord4fColor4fNormal3fVertex4fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glTexCoord4fColor4fNormal3fVertex4fvSUN( GLfloatArray(tc), GLfloatArray(c), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('tc', 'c', 'n', 'v',),
)

glReplacementCodeuiVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiVertex3fSUN( GLuint(rc), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 'x', 'y', 'z',),
)

glReplacementCodeuiVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiVertex3fvSUN( GLuintArray(rc), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'v',),
)

glReplacementCodeuiColor4ubVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiColor4ubVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLubyte, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiColor4ubVertex3fSUN( GLuint(rc), GLubyte(r), GLubyte(g), GLubyte(b), GLubyte(a), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 'r', 'g', 'b', 'a', 'x', 'y', 'z',),
)

glReplacementCodeuiColor4ubVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiColor4ubVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLubyteArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiColor4ubVertex3fvSUN( GLuintArray(rc), GLubyteArray(c), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'c', 'v',),
)

glReplacementCodeuiColor3fVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiColor3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiColor3fVertex3fSUN( GLuint(rc), GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 'r', 'g', 'b', 'x', 'y', 'z',),
)

glReplacementCodeuiColor3fVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiColor3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiColor3fVertex3fvSUN( GLuintArray(rc), GLfloatArray(c), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'c', 'v',),
)

glReplacementCodeuiNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiNormal3fVertex3fSUN( GLuint(rc), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glReplacementCodeuiNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiNormal3fVertex3fvSUN( GLuintArray(rc), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'n', 'v',),
)

glReplacementCodeuiColor4fNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiColor4fNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiColor4fNormal3fVertex3fSUN( GLuint(rc), GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(a), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 'r', 'g', 'b', 'a', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glReplacementCodeuiColor4fNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiColor4fNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiColor4fNormal3fVertex3fvSUN( GLuintArray(rc), GLfloatArray(c), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'c', 'n', 'v',),
)

glReplacementCodeuiTexCoord2fVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiTexCoord2fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiTexCoord2fVertex3fSUN( GLuint(rc), GLfloat(s), GLfloat(t), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 's', 't', 'x', 'y', 'z',),
)

glReplacementCodeuiTexCoord2fVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiTexCoord2fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiTexCoord2fVertex3fvSUN( GLuintArray(rc), GLfloatArray(tc), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'tc', 'v',),
)

glReplacementCodeuiTexCoord2fNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiTexCoord2fNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiTexCoord2fNormal3fVertex3fSUN( GLuint(rc), GLfloat(s), GLfloat(t), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 's', 't', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glReplacementCodeuiTexCoord2fNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiTexCoord2fNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiTexCoord2fNormal3fVertex3fvSUN( GLuintArray(rc), GLfloatArray(tc), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'tc', 'n', 'v',),
)

glReplacementCodeuiTexCoord2fColor4fNormal3fVertex3fSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiTexCoord2fColor4fNormal3fVertex3fSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLuint, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat, constants.GLfloat,),
	doc = 'glReplacementCodeuiTexCoord2fColor4fNormal3fVertex3fSUN( GLuint(rc), GLfloat(s), GLfloat(t), GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(a), GLfloat(nx), GLfloat(ny), GLfloat(nz), GLfloat(x), GLfloat(y), GLfloat(z) ) -> None',
	argNames = ('rc', 's', 't', 'r', 'g', 'b', 'a', 'nx', 'ny', 'nz', 'x', 'y', 'z',),
)

glReplacementCodeuiTexCoord2fColor4fNormal3fVertex3fvSUN = platform.createExtensionFunction( 
	'glReplacementCodeuiTexCoord2fColor4fNormal3fVertex3fvSUN', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLuintArray, arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray, arrays.GLfloatArray,),
	doc = 'glReplacementCodeuiTexCoord2fColor4fNormal3fVertex3fvSUN( GLuintArray(rc), GLfloatArray(tc), GLfloatArray(c), GLfloatArray(n), GLfloatArray(v) ) -> None',
	argNames = ('rc', 'tc', 'c', 'n', 'v',),
)


def glInitVertexSUN():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SUN_vertex' )
