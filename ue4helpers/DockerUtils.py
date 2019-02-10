import docker, fnmatch

class DockerUtils(object):
	'''
	Provides functionality related to Docker
	'''
	
	@staticmethod
	def start_for_exec(client, image, **kwargs):
		'''
		Starts a container in a detached state using a command that will block indefinitely
		and returns the container handle. The handle can then be used to execute commands
		inside the container. The container will be removed automatically when it is stopped,
		but it will need to be stopped manually by calling `DockerUtils.stop()`.
		'''
		# Determine if the container image is a Windows image or a Linux image
		imageOS = DockerUtils.list_images(client, image)[0].attrs['Os']
		command = ['timeout', '/t', '99999', '/nobreak'] if imageOS == 'windows' else ['bash', '-c', 'sleep infinity']
		return client.containers.run(
			image,
			command,
			stdin_open = imageOS == 'windows',
			tty = imageOS == 'windows',
			detach = True,
			remove = True,
			**kwargs
		)
	
	@staticmethod
	def exec(container, command, **kwargs):
		'''
		Executes a command in a container returned by `DockerUtils.start()` and returns the output
		'''
		result, output = container.exec_run(command, **kwargs)
		if result is not None and result != 0:
			container.stop()
			raise RuntimeError(
				'Failed to run command {} in container. Process returned exit code {} with output: {}'.format(
					command,
					result,
					output
				)
			)
		
		return output
	
	@staticmethod
	def exec_multiple(container, commands, **kwargs):
		'''
		Executes multiple commands in a container returned by `DockerUtils.start()` and prints the output
		'''
		for command in commands:
			print(DockerUtils.exec(container, command, **kwargs).decode('utf-8'))
	
	@staticmethod
	def stop(container):
		'''
		Stops a container returned by `DockerUtils.start()`
		'''
		container.stop(timeout=1)
	
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
