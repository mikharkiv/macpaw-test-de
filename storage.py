import json

import settings

PROCESSED_FILENAME = settings.dev['PROCESSED_FILES_FILENAME']
if not PROCESSED_FILENAME:
	raise KeyError('ImproperlyConfigured: settings.PROCESSED_FILES_FILENAME '
					'should be set')

try:
	with open(PROCESSED_FILENAME, 'r') as file:
		_registry = json.loads(file.read())
		if type(_registry) != list:
			_registry = []
except FileNotFoundError:
	_registry = []


def was_file_processed(filename):
	return filename in _registry


def register_file(filename):
	_registry.append(filename)
	with open(PROCESSED_FILENAME, 'w') as file_obj:
		file_obj.write(json.dumps(_registry))
