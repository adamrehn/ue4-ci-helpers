from os.path import exists, isdir, join
import itertools, os, shutil
from conans import tools
from glob import glob

class FilesystemUtils(object):
	'''
	Provides filesystem-related functionality
	'''
	
	@staticmethod
	def copy(source, dest):
		'''
		Copies the specified file or directory to the specified destination location
		'''
		if isdir(source):
			shutil.copytree(source, dest)
		else:
			shutil.copy2(source, dest)
	
	@staticmethod
	def is_uri(path):
		'''
		Determines if the specified path is a URI
		'''
		return '://' in path
	
	@staticmethod
	def read(filename, decode=True):
		'''
		Reads the contents of a file
		'''
		data = tools.load(filename, binary=True)
		return data.decode('utf-8') if decode == True else data
	
	@staticmethod
	def remove(path):
		'''
		Removes the specified file or directory if it exists
		'''
		if exists(path):
			if isdir(path):
				shutil.rmtree(path)
			else:
				os.unlink(path)
	
	@staticmethod
	def remove_matching(root, patterns):
		'''
		Removes all files and directories within the specified root directory
		that match any of the specified patterns.
		
		Returns the list of removed files and directories.
		'''
		
		# Concatenate the glob results for each of the supplied patterns
		matches = list(itertools.chain.from_iterable([
			glob(join(root, '**', pattern), recursive=True)
			for pattern in patterns
		]))
		
		# Remove all of the matching files and directories
		for match in matches:
			FilesystemUtils.remove(match)
			
		return matches
	
	@staticmethod
	def write(filename, data):
		'''
		Writes data to a file
		'''
		return tools.save(filename, data)
