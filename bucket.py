import logging

import aiohttp
import urllib.request
import settings

FILES_LIST_KEY = settings.PROFILE.get('FILES_LIST_KEY')
BUCKET_NAME = settings.PROFILE.get('BUCKET_NAME')
BUCKET_ENCODING = settings.PROFILE.get('BUCKET_ENCODING')

if not FILES_LIST_KEY or not BUCKET_NAME or not BUCKET_ENCODING:
	raise KeyError('ImproperlyConfigured: Bucket settings are incorrect')

_session = aiohttp.ClientSession()


def get_bucket_files() -> list:
	"""
	Retrieves a list of files of the given bucket by key

	:return: list of names of the files
	"""
	try:
		url = urllib.request.urlopen(f'http://{BUCKET_NAME}/{FILES_LIST_KEY}')
	except (urllib.request.HTTPError, urllib.request.URLError) as e:
		logging.critical(e)
		raise e
	data = url.read()
	return data.decode(BUCKET_ENCODING).split('\n')


async def get_bucket_file(filename: str) -> str:
	"""
	Returns contents of the file in the bucket

	:param filename: name of the file
	:return: content of the file
	"""
	async with _session.get(f'http://{BUCKET_NAME}/{filename}') as resp:
		return await resp.text()


async def close_session():
	await _session.close()
