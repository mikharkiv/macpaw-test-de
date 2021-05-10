import aiohttp
import urllib.request
import settings

FILES_LIST_KEY = settings.dev.get('FILES_LIST_KEY', None)
BUCKET_NAME = settings.dev.get('BUCKET_NAME', None)
BUCKET_ENCODING = settings.dev.get('BUCKET_ENCODING', None)

if not FILES_LIST_KEY or not BUCKET_NAME or not BUCKET_ENCODING:
	raise KeyError('Bucket settings are incorrect')

_session = aiohttp.ClientSession()


def get_bucket_files():
	url = urllib.request.urlopen(f'http://{BUCKET_NAME}/{FILES_LIST_KEY}')
	data = url.read()
	return data.decode(BUCKET_ENCODING)


async def async_get_bucket_file(filename):
	async with _session.get(f'http://{BUCKET_NAME}/{filename}') as resp:
		data = await resp.text()
		return data


async def close_session():
	await _session.close()
