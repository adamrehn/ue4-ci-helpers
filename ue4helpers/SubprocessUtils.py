import subprocess

class SubprocessUtils(object):
	'''
	Provides subprocess-related functionality
	'''
	
	@staticmethod
	def capture(command, **kwargs):
		'''
		Executes a subprocess and captures its stdout output, allowing stderr output to be printed
		'''
		result = subprocess.run(command, check=True, stdout=subprocess.PIPE, **kwargs)
		return result.stdout.decode('utf-8').strip()
	
	@staticmethod
	def run(command, **kwargs):
		'''
		Executes a subprocess and raises an exception if it terminates with a non-zero exit code
		'''
		subprocess.run(command, check=True, **kwargs)
