import json

import bucket
import db
from data import App, Movie, Song
from utils import print_elapsed_time

data_types = {
	'app': App,
	'movie': Movie,
	'song': Song
}


# @print_elapsed_time
def process_entry(entry):
	# print('Processing entry...', end=' ')
	entry_type = entry.get('type', None)
	data_class = data_types.get(entry_type, None)
	if data_class is not None:
		data_obj = data_class()
		data_obj.setup(**entry['data'])
		if data_obj.is_valid:
			db.write_data(data_obj)
		else:
			print('Invalid object!')


@print_elapsed_time
def process_file(filename):
	print('Processing file...')
	content = bucket.get_bucket_file(filename)
	entries = json.loads(content)
	for entry in entries:
		process_entry(entry)
	db.write_file_processed(filename)
	db.finish_transactions()
	print('Processing file done')


@print_elapsed_time
def main():
	files = bucket.get_files_list().split('\n')
	for file in files:
		if not db.was_file_processed(file):
			process_file(file)


if __name__ == '__main__':
	main()
