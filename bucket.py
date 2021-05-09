import boto3
from botocore import UNSIGNED
from botocore.config import Config

import settings

FILES_LIST_KEY = settings.dev.get('FILES_LIST_KEY', None)
BUCKET_NAME = settings.dev.get('BUCKET_NAME', None)
BUCKET_ENCODING = settings.dev.get('BUCKET_ENCODING', None)

if not FILES_LIST_KEY or not BUCKET_NAME or not BUCKET_ENCODING:
	raise KeyError('Bucket settings are incorrect')

__bucket = boto3.resource('s3', config=Config(signature_version=UNSIGNED))


def get_files_list() -> str:
	"""
	Retrieve list of files from S3 bucket

	:return: List of files (if available)
	"""
	return get_bucket_file(FILES_LIST_KEY)


def get_bucket_file(filename: str) -> str:
	"""
	Returns contents of given file on S3 bucket

	:param filename: Name of the file
	:return: Content of the file
	"""
	list_obj = __bucket.Object(bucket_name=BUCKET_NAME, key=filename)
	return list_obj.get()['Body'].read().decode(BUCKET_ENCODING)
