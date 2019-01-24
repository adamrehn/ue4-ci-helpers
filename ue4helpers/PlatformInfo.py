import platform

class PlatformInfo(object):
	'''
	Provides functionality related to the build platform
	'''
	
	@staticmethod
	def identifier():
		'''
		Returns a human-readable platform identifier for the host system (i.e. "Windows", "Mac", "Linux")
		'''
		identifier = platform.system()
		return 'Mac' if identifier == 'Darwin' else identifier
