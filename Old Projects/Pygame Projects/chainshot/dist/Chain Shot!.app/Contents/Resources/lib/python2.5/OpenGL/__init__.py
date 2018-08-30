"""ctypes-based OpenGL wrapper for Python

This is the PyOpenGL 3.x tree, it attempts to provide
a largely compatible API for code written with the 
PyOpenGL 2.x series using the ctypes foreign function 
interface system.

Configuration Variables:

There are a few configuration variables in this top-level
module.  Applications should be the only code that tweaks 
these variables, mid-level libraries should not take it 
upon themselves to disable/enable features at this level.
The implication there is that your library code should be 
able to work with any of the valid configurations available
with these sets of flags.

	ERROR_CHECKING -- if set to a False value before
		importing any OpenGL.* libraries will completely 
		disable error-checking.  This can dramatically
		improve performance, but makes debugging far 
		harder.
		
		This is intended to be turned off *only* in a 
		production environment where you *know* that 
		your code is entirely free of situations where you 
		use exception-handling to handle error conditions,
		i.e. where you are explicitly checking for errors 
		everywhere they can occur in your code.
		
		Default: True 

	ERROR_LOGGING -- If True, then wrap array-handler 
		functions with  error-logging operations so that all exceptions 
		will be reported to log objects in OpenGL.logs, note that 
		this means you will get lots of error logging whenever you 
		have code that tests by trying something and catching an 
		error, this is intended to be turned on only during 
		development so that you can see why something is failing.
		
		Errors are normally logged to the OpenGL.errors logger.
		
		Only triggers if ERROR_CHECKING is True
		
		Default: False
		
	ERROR_ON_COPY -- if set to a True value before 
		importing the numpy array-support module, will 
		cause array operations to raise 
		OpenGL.error.CopyError if an array operation 
		would cause a data-copy in order to match
		data-types.
		
		This feature allows for optimisation of your 
		application.  It should only be enabled during 
		testing stages to prevent raising errors on 
		recoverable conditions at run-time.  
		
		Note that this feature only works with Numpy 
		arrays at the moment.
		
		Default: False
	
	FULL_LOGGING -- If True, then wrap functions with 
		logging operations which reports each call along with its 
		arguments to  the OpenGL.calltrace logger at the INFO 
		level.  This is *extremely* slow.  You should *not* enable 
		this in production code! 
		
		You will need to have a  logging configuration (e.g. 
			logging.basicConfig() 
		) call  in your top-level script to see the results of the 
		logging.
		
		Default: False
	
	ALLOW_NUMPY_SCALARS -- if True, we will wrap 
		all GLint/GLfloat calls conversions with wrappers 
		that allow for passing numpy scalar values.
		
		Note that this is experimental, *not* reliable,
		and very slow!
		
		Note that byte/char types are not wrapped.
		
		Default: False
"""
from OpenGL.version import __version__

ERROR_CHECKING = True
ERROR_LOGGING = False
ERROR_ON_COPY = False

FULL_LOGGING = False
ALLOW_NUMPY_SCALARS = False
