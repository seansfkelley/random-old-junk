'''OpenGL extension WIN.phong_shading

Overview (from the spec)
	
	WIN_phong_shading enables rendering Phong shaded primitives using OpenGL.
	Phong shading is a well known shading technique documented 
	in most graphics texts. 
	
	As opposed to Gouraud (or smooth) shading, which simply calculates the 
	normals at the vertices and then interpolates the colors of the pixels, 
	Phong shading involves interpolating an individual normal for every pixel,
	and then applying the shading model to each pixel based on its normal 
	component. 
	
	While Phong shading requires substantially more computation than does 
	Gouraud shading, the resulting images are more realistic, especially if the
	primitives are large. 

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/WIN/phong_shading.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_PHONG_WIN = constant.Constant( 'GL_PHONG_WIN', 0x80EA )
GL_PHONG_HINT_WIN = constant.Constant( 'GL_PHONG_HINT_WIN', 0x80EB )


def glInitPhongShadingWIN():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_WIN_phong_shading' )