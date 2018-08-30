'''OpenGL extension ARB.texture_rectangle

Overview (from the spec)
	
	OpenGL texturing is limited to images with power-of-two dimensions
	and an optional 1-texel border.  The ARB_texture_rectangle extension
	adds a new texture target that supports 2D textures without requiring
	power-of-two dimensions.
	
	Non-power-of-two sized (NPOTS) textures are useful for storing video
	images that do not have power-of-two sized (POTS).  Re-sampling
	artifacts are avoided and less texture memory may be required by
	using non-power-of-two sized textures.  Non-power-of-two sized
	textures are also useful for shadow maps and window-space texturing.
	
	However, non-power-of-two sized textures have limitations that
	do not apply to power-of-two sized textures.  NPOTS textures may
	not use mipmap filtering; POTS textures support both mipmapped
	and non-mipmapped filtering.  NPOTS textures support only the
	GL_CLAMP, GL_CLAMP_TO_EDGE, and GL_CLAMP_TO_BORDER wrap modes;
	POTS textures support GL_CLAMP_TO_EDGE, GL_REPEAT, GL_CLAMP,
	GL_MIRRORED_REPEAT, and GL_CLAMP_TO_BORDER (and GL_MIRROR_CLAMP_ATI
	and GL_MIRROR_CLAMP_TO_EDGE_ATI if ATI_texture_mirror_once is
	supported) .  NPOTS textures do not support an optional 1-texel
	border; POTS textures do support an optional 1-texel border.
	
	NPOTS textures are accessed by dimension-dependent (aka
	non-normalized) texture coordinates.  So instead of thinking of
	the texture image lying in a [0..1]x[0..1] range, the NPOTS texture
	image lies in a [0..w]x[0..h] range.
	
	This extension adds a new texture target and related state (proxy,
	binding, max texture size).

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/ARB/texture_rectangle.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_TEXTURE_RECTANGLE_ARB = constant.Constant( 'GL_TEXTURE_RECTANGLE_ARB', 0x84F5 )
GL_TEXTURE_BINDING_RECTANGLE_ARB = constant.Constant( 'GL_TEXTURE_BINDING_RECTANGLE_ARB', 0x84F6 )
GL_PROXY_TEXTURE_RECTANGLE_ARB = constant.Constant( 'GL_PROXY_TEXTURE_RECTANGLE_ARB', 0x84F7 )
GL_MAX_RECTANGLE_TEXTURE_SIZE_ARB = constant.Constant( 'GL_MAX_RECTANGLE_TEXTURE_SIZE_ARB', 0x84F8 )


def glInitTextureRectangleARB():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_ARB_texture_rectangle' )
