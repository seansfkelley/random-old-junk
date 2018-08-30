'''OpenGL extension MESA.pack_invert

Overview (from the spec)
	
	This extension adds a new pixel storage parameter to indicate that
	images are to be packed in top-to-bottom order instead of OpenGL's
	conventional bottom-to-top order.  Only pixel packing can be
	inverted (i.e. for glReadPixels, glGetTexImage, glGetConvolutionFilter,
	etc).
	
	Almost all known image file formats store images in top-to-bottom
	order.  As it is, OpenGL reads images from the frame buffer in
	bottom-to-top order.  Thus, images usually have to be inverted before
	writing them to a file with image I/O libraries.  This extension
	allows images to be read such that inverting isn't needed.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/MESA/pack_invert.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_PACK_INVERT_MESA = constant.Constant( 'GL_PACK_INVERT_MESA', 0x8758 )
glget.addGLGetConstant( GL_PACK_INVERT_MESA, (1,) )


def glInitPackInvertMESA():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_MESA_pack_invert' )
