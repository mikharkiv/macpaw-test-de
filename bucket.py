import logging

import aiohttp
import urllib.request
import settings

FILES_LIST_KEY = settings.dev.get('FILES_LIST_KEY', None)
BUCKET_NAME = settings.dev.get('BUCKET_NAME', None)
BUCKET_ENCODING = settings.dev.get('BUCKET_ENCODING', None)

if not FILES_LIST_KEY or not BUCKET_NAME or not BUCKET_ENCODING:
	raise KeyError('Bucket settings are incorrect')

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
