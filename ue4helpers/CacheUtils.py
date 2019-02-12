from .FilesystemUtils import FilesystemUtils
import os, requests

class CacheUtils(object):
	'''
	Provides functionality related to using cached data in preference over remote data when available
	'''
	
	@staticmethod
	def select_cheapest(sources):
		'''
		Selects the most cost-effective available source of the resource from the supplied list and returns the path or URI.
		
		The list should be sorted in ascending order of cost (i.e. local cache files first, URIs last.)
		'''
		for source in sources:
			if CacheUtils.is_available(source) == True:
				return source
		
		raise RuntimeError('none of the specified sources are available!')
	
	@staticmethod
	def is_available(resource):
		'''
		Determines if the specified resource is available (file exists, URI is accessible, etc.)
		'''
		return CacheUtils.uri_available(resource) if FilesystemUtils.is_uri(resource) else CacheUtils.file_available(resource)
	
	@staticmethod
	def file_available(path):
		'''
		Determines if the specified file exists
		'''
		return os.path.exists(path)
	
	@staticmethod
	def uri_available(uri):
		'''
		Determines if the specified URI exists and is accessible
		'''
		try:
			response = requests.head(uri, allow_redirects=True)
			return response.status_code == 200
		except:
			return False
