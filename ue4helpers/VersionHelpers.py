from .SubprocessUtils import SubprocessUtils
import platform

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
		return lambda root, descriptor: VersionHelpers._extract_git_commit_date(root)
	
	
	# "Private" methods
	
	@staticmethod
	def _extract_git_commit_date(repo):
		'''
		Extracts the date from the most recent git commit in the specified repository
		'''
		date = SubprocessUtils.capture(['git', 'log', '-n', '1', '--format=format:%ai'], cwd=repo)
		return date.split(' ')[0].replace('-', '')
