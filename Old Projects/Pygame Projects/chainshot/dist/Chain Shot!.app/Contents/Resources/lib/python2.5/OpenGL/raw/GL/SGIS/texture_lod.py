'''OpenGL extension SGIS.texture_lod

Overview (from the spec)
	
	This extension imposes two constraints related to the texture level of
	detail parameter LOD, which is represented by the Greek character lambda
	in the GL Specification.  One constraint clamps LOD to a specified
	floating point range.  The other limits the selection of mipmap image
	arrays to a subset of the arrays that would otherwise be considered.
	
	Together these constraints allow a large texture to be loaded and
	used initially at low resolution, and to have its resolution raised
	gradually as more resolution is desired or available.  Image array
	specification is necessarily integral, rather than continuous.  By
	providing separate, continuous clamping of the LOD parameter, it is
	possible to avoid "popping" artifacts when higher resolution images
	are provided.
	
	Note: because the shape of the mipmap array is always determined by
	the dimensions of the level 0 array, this array must be loaded for
	mipmapping to be active.  If the level 0 array is specified with a
	null image pointer, however, no actual data transfer will take
	place.  And a sufficiently tuned implementation might not even
	allocate space for a level 0 array so specified until true image
	data were presented.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/SGIS/texture_lod.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_TEXTURE_MIN_LOD_SGIS = constant.Constant( 'GL_TEXTURE_MIN_LOD_SGIS', 0x813A )
GL_TEXTURE_MAX_LOD_SGIS = constant.Constant( 'GL_TEXTURE_MAX_LOD_SGIS', 0x813B )
GL_TEXTURE_BASE_LEVEL_SGIS = constant.Constant( 'GL_TEXTURE_BASE_LEVEL_SGIS', 0x813C )
GL_TEXTURE_MAX_LEVEL_SGIS = constant.Constant( 'GL_TEXTURE_MAX_LEVEL_SGIS', 0x813D )


def glInitTextureLodSGIS():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_SGIS_texture_lod' )