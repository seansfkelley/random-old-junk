'''OpenGL extension APPLE.ycbcr_422

Overview (from the spec)
	
	This extension provides a method for GL to read, store and optionally
	process textures that are defined in Y'CbCr 422 video formats.  This
	extension supports the two common Y'CbCr 422 video formats (known by
	QuickTime FourCC as '2vuy' and 'yuvs'). These formats represent one of the
	most common 16 bit Y'CbCr formats in both standard and reverse byte
	ordering. From a client stand point these can be assumed to be decoded
	immediately (even though the implementation is free to optimize the data
	storage and keep it in the native format) and otherwise function as any
	other texture format.  The texture command <internalformat> parameter
	normally be should be specified as RGB, since Y'CbCr is just a form of RGB
	data.  This extension can be supported with either hardware or software
	decoding and it is up to the specific implementation to determine which is
	used.
	
	A new <format> is added, YCBCR_422_APPLE.  Additionally, to handle the
	difference in pixel size and byte ordering for 422 video, the pixel storage
	operations treat YCBCR_422_APPLE as a 2 component format using
	the UNSIGNED_SHORT_8_8_APPLE or UNSIGNED_SHORT_8_8_REV_APPLE <type>.
	
	The '2vuy' or k2vuyPixelFormat pixel format is an 8-bit 4:2:2 Component
	Y'CbCr format. Each 16 bit pixel is represented by an unsigned eight bit
	luminance component and two unsigned eight bit chroma components. Each pair
	of pixels shares a common set of chroma values. The components are ordered
	in memory; Cb, Y0, Cr, Y1. The luminance components have a range of [16,
	235], while the chroma value has a range of [16, 240]. This is consistent
	with the CCIR601 spec. This format is fairly prevalent on both Mac and Win32
	platforms. The equivalent Microsoft fourCC is OUYVY�.  This format is
	supported with the UNSIGNED_SHORT_8_8_REV_APPLE type for pixel storage
	operations.
	
	The 'yuvs' or kYUVSPixelFormat is an 8-bit 4:2:2 Component Y'CbCr format.
	Identical to the k2vuyPixelFormat except each 16 bit word has been byte
	swapped. This results in a component ordering of; Y0, Cb, Y1, Cr. This is
	most prevalent yuv 4:2:2 format on both Mac and Win32 platforms. The
	equivalent Microsoft fourCC is 'YUY2'.  This format is supported with the
	UNSIGNED_SHORT_8_8_APPLE type for pixel storage operations.

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/APPLE/ycbcr_422.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_YCBCR_422_APPLE = constant.Constant( 'GL_YCBCR_422_APPLE', 0x85B9 )
GL_UNSIGNED_SHORT_8_8_APPLE = constant.Constant( 'GL_UNSIGNED_SHORT_8_8_APPLE', 0x85BA )
GL_UNSIGNED_SHORT_8_8_REV_APPLE = constant.Constant( 'GL_UNSIGNED_SHORT_8_8_REV_APPLE', 0x85BB )


def glInitYcbcr422APPLE():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_APPLE_ycbcr_422' )
