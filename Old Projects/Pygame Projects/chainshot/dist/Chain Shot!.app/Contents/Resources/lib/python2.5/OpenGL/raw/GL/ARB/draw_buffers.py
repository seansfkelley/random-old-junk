'''OpenGL extension ARB.draw_buffers

Overview (from the spec)
	
	This extension extends ARB_fragment_program and ARB_fragment_shader
	to allow multiple output colors, and provides a mechanism for
	directing those outputs to multiple color buffers.
	

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/ARB/draw_buffers.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
GL_MAX_DRAW_BUFFERS_ARB = constant.Constant( 'GL_MAX_DRAW_BUFFERS_ARB', 0x8824 )
glget.addGLGetConstant( GL_MAX_DRAW_BUFFERS_ARB, (1,) )
GL_DRAW_BUFFER0_ARB = constant.Constant( 'GL_DRAW_BUFFER0_ARB', 0x8825 )
GL_DRAW_BUFFER1_ARB = constant.Constant( 'GL_DRAW_BUFFER1_ARB', 0x8826 )
GL_DRAW_BUFFER2_ARB = constant.Constant( 'GL_DRAW_BUFFER2_ARB', 0x8827 )
GL_DRAW_BUFFER3_ARB = constant.Constant( 'GL_DRAW_BUFFER3_ARB', 0x8828 )
GL_DRAW_BUFFER4_ARB = constant.Constant( 'GL_DRAW_BUFFER4_ARB', 0x8829 )
GL_DRAW_BUFFER5_ARB = constant.Constant( 'GL_DRAW_BUFFER5_ARB', 0x882A )
GL_DRAW_BUFFER6_ARB = constant.Constant( 'GL_DRAW_BUFFER6_ARB', 0x882B )
GL_DRAW_BUFFER7_ARB = constant.Constant( 'GL_DRAW_BUFFER7_ARB', 0x882C )
GL_DRAW_BUFFER8_ARB = constant.Constant( 'GL_DRAW_BUFFER8_ARB', 0x882D )
GL_DRAW_BUFFER9_ARB = constant.Constant( 'GL_DRAW_BUFFER9_ARB', 0x882E )
GL_DRAW_BUFFER10_ARB = constant.Constant( 'GL_DRAW_BUFFER10_ARB', 0x882F )
GL_DRAW_BUFFER11_ARB = constant.Constant( 'GL_DRAW_BUFFER11_ARB', 0x8830 )
GL_DRAW_BUFFER12_ARB = constant.Constant( 'GL_DRAW_BUFFER12_ARB', 0x8831 )
GL_DRAW_BUFFER13_ARB = constant.Constant( 'GL_DRAW_BUFFER13_ARB', 0x8832 )
GL_DRAW_BUFFER14_ARB = constant.Constant( 'GL_DRAW_BUFFER14_ARB', 0x8833 )
GL_DRAW_BUFFER15_ARB = constant.Constant( 'GL_DRAW_BUFFER15_ARB', 0x8834 )
glDrawBuffersARB = platform.createExtensionFunction( 
	'glDrawBuffersARB', dll=platform.GL,
	resultType=None, 
	argTypes=(constants.GLsizei, arrays.GLuintArray,),
	doc = 'glDrawBuffersARB( GLsizei(n), GLuintArray(bufs) ) -> None',
	argNames = ('n', 'bufs',),
)


def glInitDrawBuffersARB():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( 'GL_ARB_draw_buffers' )