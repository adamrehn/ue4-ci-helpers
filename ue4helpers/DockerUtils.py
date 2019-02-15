import docker, fnmatch, posixpath, ntpath, os, sys, tempfile
from .ArchiveUtils import ArchiveUtils

class DockerUtils(object):
	'''
	Provides functionality related to Docker
	'''
	
	# Image-related functionality
	
	@staticmethod
	def image_platform(client, image):
		'''
		Retrieves the platform identifier for the specified image
		'''
		return DockerUtils.list_images(client, image)[0].attrs['Os']
	
	@staticmethod
	def list_images(client, tagFilter = None, filters = {}):
		'''
		Retrieves the details for each image matching the specified filters
		'''
		
		# Retrieve the list of images matching the specified filters
		images = client.images.list(filters=filters)
		
		# Apply our tag filter if one was specified
		if tagFilter is not None:
			images = [i for i in images if len(i.tags) > 0 and len(fnmatch.filter(i.tags, tagFilter)) > 0]
		
		return images
	
	
	# Container-related functionality
	
	@staticmethod
	def container_platform(container):
		'''
		Retrieves the platform identifier for the specified container
		'''
		return container.attrs['Platform']
	
	@staticmethod
	def copy_to_host(container, container_path, host_path):
		'''
		Copies a file or directory from a container returned by `DockerUtils.start()` to the host system.
		
		`container_path` is the absolute path to the file or directory in the container.
		
		`host_path` is the absolute path to the directory on the host system where the copied files will be placed.
		'''
		
		# Create a temporary file to hold the .tar archive data
		with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as tempArchive:
			
			# Copy the data from the container to the temporary archive
			chunks, stat = container.get_archive(container_path)
			for chunk in chunks:
				tempArchive.write(chunk)
			
			# Extract the file to the host system destination
			tempArchive.close()
			ArchiveUtils.extract(tempArchive.name, host_path, remove=False)
			os.unlink(tempArchive.name)
	
	@staticmethod
	def exec(container, command, **kwargs):
		'''
		Executes a command in a container returned by `DockerUtils.start()` and streams the output
		'''
		
		# Attempt to start the command
		details = container.client.api.exec_create(container.id, command, **kwargs)
		output = container.client.api.exec_start(details['Id'], stream=True, demux=True)
		
		# Stream the output
		for chunk in output:
			
			# Isolate the stdout and stderr chunks
			stdout, stderr = chunk
			
			# Print the stderr data if we have any
			if stderr is not None:
				print(stderr.decode('utf-8'), end='', flush=True, file=sys.stderr)
			
			# Print the stdout data if we have any
			if stdout is not None:
				print(stdout.decode('utf-8'), end='', flush=True, file=sys.stdout)
		
		# Determine if the command succeeded
		result = container.client.api.exec_inspect(details['Id'])['ExitCode']
		if result != 0:
			container.stop()
			raise RuntimeError('Failed to run command {} in container. Process returned exit code {}.'.format(
				command,
				result
			))
	
	@staticmethod
	def exec_multiple(container, commands=[], pre_hook=None, post_hook=None, **kwargs):
		'''
		Executes multiple commands in a container returned by `DockerUtils.start()` and streams the output
		'''
		
		# If no pre-execution and post-execution hooks were provided, set them to no-ops
		pre_hook = pre_hook if pre_hook is not None else lambda cmd: None
		post_hook = post_hook if post_hook is not None else lambda cmd: None
		
		# Execute each of our commands, executing the hooks as appropriate
		for command in commands:
			pre_hook(command)
			DockerUtils.exec(container, command, **kwargs)
			post_hook(command)
	
	@staticmethod
	def join_path(container, a, *p):
		'''
		Equivalent to `os.path.join`, but uses the path conventions for the platform of the specified container
		'''
		platform = DockerUtils.container_platform(container)
		return ntpath.join(a, p) if platform == 'windows' else posixpath.join(a, p)
	
	@staticmethod
	def start_for_exec(client, image, **kwargs):
		'''
		Starts a container in a detached state using a command that will block indefinitely
		and returns the container handle. The handle can then be used to execute commands
		inside the container. The container will be removed automatically when it is stopped,
		but it will need to be stopped manually by calling `DockerUtils.stop()`.
		'''
		platform = DockerUtils.image_platform(client, image)
		command = ['timeout', '/t', '99999', '/nobreak'] if platform == 'windows' else ['bash', '-c', 'sleep infinity']
		return client.containers.run(
			image,
			command,
			stdin_open = platform == 'windows',
			tty = platform == 'windows',
			detach = True,
			remove = True,
			**kwargs
		)
	
	@staticmethod
	def stop(container):
		'''
		Stops a container returned by `DockerUtils.start()`
		'''
		container.stop(timeout=1)
	
	@staticmethod
	def workspace_dir(container):
		'''
		Returns a platform-appropriate workspace path for a container returned by `DockerUtils.start()`
		'''
		platform = DockerUtils.container_platform(container)
		return 'C:\\workspace' if platform == 'windows' else '/tmp/workspace'
