from os.path import basename, join, splitext
from conans import tools
from glob import glob
import json

class DescriptorData(object):
	'''
	Provides functionality for parsing Unreal descriptor files
	'''
	
	@staticmethod
	def from_directory(directory, extension):
		'''
		Locates the descriptor file located in the specified directory and parses it.
		The return value is a dictionary containing the parsed JSON data, with an
		additional key called `Name` that contains the name of the descriptor file
		with the file extension removed.
		'''
		
		# Verify that there is a descriptor file in the specified directory
		descriptors = glob(join(directory, '*{}'.format(extension)))
		if len(descriptors) == 0:
			raise RuntimeError('could not find a `{}` descriptor file in the directory "{}"'.format(
				extension,
				directory
			))
		
		# Parse the descriptor JSON data
		descriptor = descriptors[0]
		data = json.loads(tools.load(descriptor))
		
		# Inject the descriptor's name into the parsed data
		data['Name'] = splitext(basename(descriptor))[0]
		return data
