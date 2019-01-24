from .FilesystemUtils import FilesystemUtils
from .SubprocessUtils import SubprocessUtils
import json, subprocess, tempfile
from conans import tools
from os.path import join

# The template contents for generated conanfile.txt files
CONANFILE_TEMPLATE = '''
[requires]
{}

[generators]
json
'''

class ConanUtils(object):
	'''
	Provides functionality related to Conan and conan-ue4cli
	'''
	
	@staticmethod
	def copy_package(package, destination):
		'''
		Copies the contents of a Conan package to the specified destination directory.
		The destination directory will be removed if it already exists.
		'''
		
		# Create an auto-deleting temporary directory to hold our generated files
		with tempfile.TemporaryDirectory() as tempDir:
			
			# Create a conanfile.txt to consume the specified package
			tools.save(join(tempDir, 'conanfile.txt'), CONANFILE_TEMPLATE.format(package))
			
			# Use `conan install` to generate the JSON file with the package details
			# (Suppress stdout output but let any stderr output be printed)
			SubprocessUtils.capture(['conan', 'install', '.', '--profile', 'ue4'], cwd=tempDir)
			
			# Parse the generated conanbuildinfo.json
			dependencies = json.loads(tools.load(join(tempDir, 'conanbuildinfo.json')))
			
			# Extract the root path to the package in Conan's local package cache
			name = package.split('/')[0]
			source = [dep['rootpath'] for dep in dependencies['dependencies'] if dep['name'] == name][0]
			
			# Copy the package contents to the destination directory
			FilesystemUtils.remove(destination)
			FilesystemUtils.copy(source, destination)
