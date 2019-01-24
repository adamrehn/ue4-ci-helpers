from .ArchiveUtils import ArchiveUtils
from .DescriptorData import DescriptorData
from .FilesystemUtils import FilesystemUtils
from .PlatformInfo import PlatformInfo
from os.path import isdir, join
import os, shutil, subprocess

class PackagerBase(object):
	'''
	Provides base functionality for packaging Unreal projects and plugins.
	This class should not be used directly. Instead, use `ProjectPackager` for
	packaging projects and `PluginPackager` for packaging plugins.
	'''
	
	def __init__(self, root, version, archive='{name}-{version}-{platform}', strip_debug=False, strip_manifests=False, stage=[], verbose=True):
		'''
		Called by our concrete subclasses. The meanings of the parameters are as follows:
		
		`root` specifies the path to the root directory of the project.
		
		`version` specifies either the version string to use or a function that accepts the root
		directory and descriptor data as parameters and returns the computed version string. The
		`VersionHelpers` class provides a number of such functions for common use cases.
		
		`archive` specifies the template string used for generating the .zip filename
		for compressing the packaged distribution. The following variables are supported:
		
		- `{name}` will expand to the descriptor filename with the file extension removed
		- `{version}` will expand to the version string derived from the `version` parameter
		- `{platform}` will expand to the platform name (i.e. "Windows", "Mac", "Linux")
		
		`strip_debug` specifies whether debug symbols should be stripped from the packaged distribution.
		
		`strip_manifests` specifies whether manifest files should be stripped from the packaged distribution.
		
		`stage` specifies a list of additional files and directories that should be copied from
		the root directory into the packaged distribution. Relative paths are maintained. Note that
		the same functionality can be achieved for projects by using the `RuntimeDependencies.Add()`
		function in the module build rules, and for plugins by using the file `FilterPlugin.ini`
		
		`verbose` specifies whether verbose output should be enabled for all of the packaging steps.
		Note that this can be overridden on a per-step basis using the optional `verbose` override
		argument of any given step.
		'''
		
		# Parse the descriptor file for the root directory before we do anything else
		self._root = root
		self._descriptor = DescriptorData.from_directory(self._root, self._extension())
		
		# Store the version string, calling the supplied function if one was provided
		self._version = version(self._root, self._descriptor) if callable(version) == True else version
		
		# Expand any variables in the archive filename template string
		self._archive = self._expand_template(archive)
		
		# Keep track of whether or not we are stripping debug symbols and manifests
		self._strip_debug = strip_debug
		self._strip_manifests = strip_manifests
		
		# Store the list of additional files and directories to stage
		self._stage = stage
		
		# Keep track of whether or not verbose output is enabled
		self._verbose = verbose
	
	def clean(self, preserve=False, verbose=None):
		'''
		Cleans any build artifacts leftover from a previous packaging run.
		The "dist" subdirectory will be always be removed, along with
		any .zip file matching our archive filename template string.
		
		If the `preserve` argument is set to False then the `ue4 clean`
		command will be run to clean any build artifacts residing outside
		of the "dist" subdirectory (i.e. the Binaries and Intermediate
		subdirectories will be removed.) You can set `preserve` to True to
		keep these files, which can be useful when merging prebuilt binaries
		from another platform with new binaries for the current platform.
		
		The `verbose` argument can be used to override the verbose output
		setting that was set in the packager's constructor.
		'''
		
		# Print progress information if verbose output is enabled
		self._progress(verbose, 'Cleaning any existing build artifacts...')
		
		# Clean packaging artifacts
		FilesystemUtils.remove(join(self._root, 'dist'))
		FilesystemUtils.remove(join(self._root, '{}.zip'.format(self._archive)))
		
		# Unless requested otherwise, clean all build artifacts as well
		if preserve == False:
			subprocess.run(['ue4', 'clean'], cwd=self._root, check=True)
	
	def package(self, args=[], verbose=None):
		'''
		Performs packaging, placing the packaged distribution in the "dist" subdirectory.
		The `args` parameter can be used to specify any additional arguments to pass to the
		`ue4 package` command, which will in turn be passed to the Unreal AutomationTool.
		If debug symbols and/or manifest files are being stripped, the relevant files will
		be removed after any additional files or directories have been staged. (This ensures
		debug symbols are stripped from the additional staged files as well, minimising output
		distribution size.)
		
		The `verbose` argument can be used to override the verbose output
		setting that was set in the packager's constructor.
		'''
		
		# Print progress information if verbose output is enabled
		self._progress(verbose, 'Performing packaging...')
		
		# Perform packaging
		subprocess.run(['ue4', 'package'] + args, cwd=self._root, check=True)
		
		# Stage any additional files or directories
		for item in self._stage:
			
			# Print progress information if verbose output is enabled
			self._progress(verbose, 'Staging "{}"...'.format(item))
			
			# Stage the file or directory, maintaining its relative path
			source = join(self._root, item)
			dest = join(self._root, 'dist', item)
			FilesystemUtils.copy(source, dest)
		
		# Strip debug symbols and/or manifest files if requested
		filters = self._strip_filters()
		if len(filters) > 0:
			
			# Print progress information if verbose output is enabled
			self._progress(verbose, 'Stripping {}...'.format(self._strip_description()))
			
			# Remove all relevant files
			stripped = FilesystemUtils.remove_matching(join(self._root, 'dist'), filters)
			
			# Print the list of removed files if verbose output is enabled
			self._progress(verbose, '\n'.join(
				['Removed file "{}".'.format(f) for f in stripped]
			))
	
	def archive(self, verbose=None):
		'''
		Compresses the packaged distribution into a .zip file and returns the archive filename.
		
		The `verbose` argument can be used to override the verbose output
		setting that was set in the packager's constructor.
		'''
		
		# Print progress information if verbose output is enabled
		self._progress(verbose, 'Compressing the packaged distribution...')
		
		# If the "dist" directory contains only a single subdirectory then we use that as the archive root
		archiveRoot = join(self._root, 'dist')
		contents = list([join(archiveRoot, item) for item in os.listdir(archiveRoot)])
		if len(contents) == 1 and isdir(contents[0]):
			archiveRoot = contents[0]
		
		# Compress the packaged distribution
		return ArchiveUtils.compress(join(self._root, self._archive), 'zip', archiveRoot)
	
	
	# "Private" methods
	
	def _extension(self):
		'''
		Returns the file extension for the descriptor files supported by this packager type.
		This function must be implemented by all concrete subclasses.
		'''
		raise NotImplementedError()
	
	def _expand_template(self, template):
		'''
		Expands variables in an archive filename template string
		'''
		template = template.replace('{name}', self._descriptor['Name'])
		template = template.replace('{version}', self._version)
		template = template.replace('{platform}', PlatformInfo.identifier())
		return template
	
	def _progress(self, verbose, message):
		'''
		Prints a progress message if verbose output is enabled
		'''
		output = verbose if verbose is not None else self._verbose
		if output == True:
			print(message)
	
	def _strip_description(self):
		'''
		Returns the description of the types of files that we are stripping
		from packaged distributions, based on our settings for stripping
		debug symbols and manifest files.
		'''
		items = []
		
		if self._strip_debug == True:
			items.append('debug symbols')
		
		if self._strip_manifests == True:
			items.append('manifest files')
		
		return ' and '.join(items)
	
	def _strip_filters(self):
		'''
		Returns the list of file filters for the files that should be stripped
		from packaged distributions, based on our settings for stripping
		debug symbols and manifest files.
		'''
		filters = []
		
		if self._strip_debug == True:
			filters.extend(['*.pdb', '*.dsym', '*.debug', '*.sym'])
		
		if self._strip_manifests == True:
			filters.extend(['Manifest_*.txt'])
		
		return filters
