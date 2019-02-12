from .GitUtils import GitUtils

class VersionHelpers(object):
	'''
	Provides functionality for automatically determining the version string for an Unreal project or plugin
	'''
	
	@staticmethod
	def from_descriptor():
		'''
		Reads the version information from the project or plugin descriptor data
		'''
		return lambda root, descriptor: descriptor['VersionName']
	
	@staticmethod
	def from_git_commit():
		'''
		Formats the date of the most recent git commit in a repository for use as a version string
		'''
		return lambda root, descriptor: GitUtils.commit_date(root)
	
	@staticmethod
	def from_git_tag():
		'''
		Returns the currently checked out tag of a git repository for use as a version string
		'''
		return lambda root, descriptor: GitUtils.tag_name(root)
