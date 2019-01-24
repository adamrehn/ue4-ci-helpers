from .PackagerBase import PackagerBase

class ProjectPackager(PackagerBase):
	'''
	Provides functionality for packaging an Unreal project.
	'''
	
	def __init__(self, root, version, archive='{name}-{version}-{platform}', strip_debug=False, strip_manifests=False, stage=[], verbose=True):
		'''
		Creates a new ProjectPackager with the specified configuration.
		
		See `PackagerBase.__init__()` for details on the input parameters.
		'''
		super().__init__(root, version, archive, strip_debug, strip_manifests, stage, verbose)
	
	
	# "Private" methods
	
	def _extension(self):
		'''
		Returns the file extension for the descriptor files supported by this packager type
		'''
		return '.uproject'
