from .ArchiveUtils import ArchiveUtils
from .SubprocessUtils import SubprocessUtils
from os.path import join

class UnrealUtils(object):
	'''
	Provides functionality related to the Unreal Engine itself
	'''
	
	@staticmethod
	def engine_root():
		'''
		Returns the root path of the current Unreal Engine installation
		'''
		return SubprocessUtils.capture(['ue4', 'root']).strip()
	
	@staticmethod
	def install_plugin(archive, name, prefix=''):
		'''
		Extracts a prebuilt Engine plugin and copies it into the Engine source tree
		'''
		ArchiveUtils.extract(archive, UnrealUtils.plugin_dir(name, prefix))
	
	@staticmethod
	def plugin_dir(plugin, prefix=''):
		'''
		Returns a path suitable for use as a destination when extracting a
		prebuilt Engine plugin and copying it into the Engine source tree.
		'''
		return join(UnrealUtils.engine_root(), 'Engine', 'Plugins', prefix, plugin)
