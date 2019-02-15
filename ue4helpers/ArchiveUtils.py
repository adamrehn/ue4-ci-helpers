from .FilesystemUtils import FilesystemUtils
from conans import tools
import shutil

class ArchiveUtils(object):
	'''
	Provides functionality related to archive files (e.g. .zip, .tar, etc.)
	'''
	
	@staticmethod
	def compress(base_name, format, root_dir=None, **kwargs):
		'''
		This function is simply a wrapper for `shutil.make_archive`.
		'''
		return shutil.make_archive(base_name, format, root_dir, **kwargs)
	
	@staticmethod
	def extract(archive, destination, remove=True):
		'''
		Extracts the specified archive to the specified destination directory.
		If the archive name is a URL then it will be downloaded to a temporary
		location and removed after extraction is complete. If the destination
		directory already exists then it will be deleted prior to extraction,
		unless `remove` is set to False.
		'''
		
		# Remove the destination directory if it already exists
		if remove == True:
			FilesystemUtils.remove(destination)
		
		# Extract the archive, downloading it first if it is a URL
		if FilesystemUtils.is_uri(archive):
			tools.get(archive, destination=destination)
		else:
			tools.unzip(archive, destination)
