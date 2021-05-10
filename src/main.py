import asyncio
import os
from datetime import datetime
import json
import logging
import time

import registry
import bucket
import db
import settings
from data import App, Movie, Song

# Maps data types in given JSON to data classes
data_types = {
	'app': App,
	'movie': Movie,
	'song': Song
}


def process_object(obj):
	entry_type = obj.get('type', None)
	data_class = data_types.get(entry_type, None)
	if data_class is not None:
		data_obj = data_class()
		data_obj.setup(**obj['data'])
		return data_obj


# Processes objects and returns only valid ones
def get_objects(raw_content):
	objects = json.loads(raw_content)
	processed_objects = map(process_object, objects)
	valid_objects = filter(lambda x: x is not None and x.is_valid,
							processed_objects)
	return list(valid_objects)


async def process_file(filename):
	logging.info(f'Processing file {filename}')
	content = await bucket.get_bucket_file(filename)
	entries = get_objects(content)
	db.write_objects(entries)
	registry.register_file(filename)


# Set up logging to console and, if needed, to file
def setup_logging():
	log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
	formatter = logging.Formatter(log_format, datefmt='%H:%M:%S')
	logging.basicConfig(datefmt=formatter.datefmt, format=log_format,
						level=logging.INFO)

	if settings.PROFILE.getboolean('SAVE_LOG'):
		# Setup logger's file handler to save in `logs/_date_.log`
		filename = datetime.now().strftime('logs/%Y-%m-%d_%H-%M-%S.log')
		log_path = os.path.abspath(os.path.join(__file__, '..\\..\\', filename))
		# Create dirs structure, if not exists
		os.makedirs(os.path.dirname(log_path), exist_ok=True)
		file_handler = logging.FileHandler(log_path)
		file_handler.setFormatter(formatter)
		logging.getLogger().addHandler(file_handler)

	logging.info('Start processing')


async def main():
	setup_logging()
	start_time = time.time()
	files = bucket.get_bucket_files()

	# Get files which wasn't yet processed
	files = list(filter(lambda x: not registry.was_file_processed(x), files))
	logging.info(f'{len(files)} files to process')

	tasks = [process_file(file) for file in files]
	await asyncio.gather(*tasks)
	db.commit()
	await bucket.close_session()
	logging.info('Done in {:.4f} seconds'.format(time.time() - start_time))


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
