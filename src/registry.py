import json
import logging
import os

from src import settings

FORCE_FILES = settings.ARGS.force
PROCESSED_FILENAME = settings.PROFILE.get('PROCESSED_FILES_FILENAME')
if not PROCESSED_FILENAME:
	raise KeyError('ImproperlyConfigured: PROCESSED_FILES_FILENAME should be set')
PROCESSED_FILE = os.path.abspath(os.path.join(__file__, '..\\..\\' + PROCESSED_FILENAME))

try:
	with open(PROCESSED_FILE, 'r') as file:
		_registry = json.loads(file.read())
		if type(_registry) != list:
			logging.warning('Processed files registry is corrupt.'
							'Processing all files...')
			_registry = []
except FileNotFoundError:
	_registry = []


def was_file_processed(filename):
	"""
	:param filename: name of the file
	:return: whether this file was already processed
	"""
	return False if FORCE_FILES else filename in _registry


def register_file(filename):
	"""
	Registers given filename (marks as processed)
	:param filename: name of the file
	"""
	_registry.append(filename)
	with open(PROCESSED_FILE, 'w') as file_obj:
		file_obj.write(json.dumps(_registry))
