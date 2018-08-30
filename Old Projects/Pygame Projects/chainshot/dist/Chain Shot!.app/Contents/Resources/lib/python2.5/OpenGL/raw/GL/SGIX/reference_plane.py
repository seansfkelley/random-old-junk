'''OpenGL extension SGIX.reference_plane

Overview (from the spec)
	
	This extension allows a group of coplanar primitives to be rendered
	without depth-buffering artifacts.  This is accomplished by generating
	the depth values for all the primitives from a single ``reference plane''
	rather than from the primitives themselves.  This ensures that all the
	primitives in the group have exactly the same depth value at any given
	sample point, no matter what imprecision may exist in the original
	specifications of the primitives or in the GL's coordinate transformation
	process.
	
	The reference plane is defined by a four-component plane equation.
	When glReferencePlaneSGIX is called, equation is transformed by the
	transpose-adjoint of a matrix that is the complete object-coordinate
	to clip-coordinate transformation.  The resulting clip-coordinate
	coefficients are transformed by the current viewport when the reference
	plane is enabled.
	
	The reference plane is enabled and disabled with glEnable and glDisable.
	
	If the reference plane is enabled, a fragment (xf,yf,zf) will have a
	new z coordinate generated from (xf,yf) by giving it the same z value
	that the reference plane would have at (xf,yf).

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SGIX/reference_plane.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_REFERENCE_PLANE_SGIX = constant.Constant( 'GL_REFERENCE_PLANE_SGIX', 0x817D )
GL_REFERENCE_PLANE_EQUATION_SGIX = constant.Constant( 'GL_REFERENCE_PLANE_EQUATION_SGIX', 0x817E )
glReferencePlaneSGIX = platform.createExtensionFunction( 
	'glReferencePlaneSGIX', dll=platform.GL,
	resultType=None, 
	argTypes=(arrays.GLdoubleArray,),
	doc = 'glReferencePlaneSGIX( GLdoubleArray(equation) ) -> None',
	argNames = ('equation',),
)


def glInitReferencePlaneSGIX():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SGIX_reference_plane' )
