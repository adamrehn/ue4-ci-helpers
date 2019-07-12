from google.cloud import storage

class GCPUtils(object):
	'''
	Provides functionality related to Google Cloud Platform (GCP)
	'''
	
	# Google Cloud Storage (GCS) utilities
	
	@staticmethod
	def download_file(bucket, key, filename):
		'''
		Downloads a file from GCS.
		
		`bucket` is the GCS Bucket name to download from.
		`key` is the key for the data that will be downloaded.
		`filename` is the path to the file that will receive the downloaded data.
		'''
		gcs = storage.Client()
		gcs.get_bucket(bucket).get_blob(key).download_to_filename(filename)
	
	@staticmethod
	def upload_file(bucket, key, filename):
		'''
		Uploads a file to GCS.
		
		`bucket` is the GCS Bucket name to upload to.
		`key` is the key to assign to the uploaded data.
		`filename` is the path to the file containing the data that will be uploaded.
		'''
		bucket = storage.Client().get_bucket(bucket)
		blob = bucket.get_blob(key)
		blob = blob if blob is not None else bucket.blob(key)
		blob.upload_from_filename(filename)
