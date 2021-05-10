import asyncio
import json
import time

import bucket
import db
import storage
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
	valid_objects = filter(lambda x: x is not None and x.is_valid, processed_objects)
	return list(valid_objects)


async def process_file(filename):
	print('Processing file', filename)
	content = await bucket.get_bucket_file(filename)
	entries = get_objects(content)
	db.write_objects(entries)
	storage.register_file(filename)


async def main():
	start_time = time.time()
	files = bucket.get_bucket_files()
	# Get files which wasn't yet processed
	files = list(filter(lambda x: not storage.was_file_processed(x), files))
	if not files:
		print('No files to process')

	tasks = [process_file(file) for file in files]
	await asyncio.gather(*tasks)
	db.commit()
	await bucket.close_session()
	print('Done in {:.4f} seconds'.format(time.time() - start_time))


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
