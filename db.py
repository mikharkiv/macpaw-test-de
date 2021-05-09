import sqlite3

import settings
from data import App, Song, Movie

TABLE_NAMES = {
	App: 'apps',
	Song: 'songs',
	Movie: 'movies'
}

CREATE_TABLE_SONGS = '''
CREATE TABLE IF NOT EXISTS songs (
	artist_name TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER NOT NULL,
	`release` TEXT NOT NULL,
	ingestion_time TEXT NOT NULL,
	PRIMARY KEY (artist_name, title)
);'''

CREATE_TABLE_MOVIES = '''
CREATE TABLE IF NOT EXISTS movies (
	original_title TEXT NOT NULL,
	original_language TEXT NOT NULL,
	budget INTEGER NOT NULL,
	is_adult INTEGER NOT NULL,
	release_date TEXT NOT NULL,
	original_title_normalized TEXT NOT NULL,
	PRIMARY KEY (original_title_normalized, release_date)
);'''

CREATE_TABLE_APPS = '''
CREATE TABLE IF NOT EXISTS apps (
	name TEXT NOT NULL,
	genre TEXT NOT NULL,
	rating REAL NOT NULL,
	version TEXT NOT NULL,
	size_bytes INTEGER NOT NULL,
	is_awesome INTEGER NOT NULL,
	PRIMARY KEY (name, version)
);'''

CREATE_TABLE_FILES = '''
CREATE TABLE IF NOT EXISTS files (
	file_name TEXT NOT NULL,
	PRIMARY KEY (file_name)
);'''

INSERT_TEMPLATE = 'INSERT INTO {} VALUES ({})'
INSERT_FULL_TEMPLATE = 'INSERT INTO {} ({}) VALUES ({})'

DB_NAME = settings.dev.get('DATABASE_NAME', None)

if not DB_NAME:
	raise KeyError('Database name should be specified')

_connection = sqlite3.connect(DB_NAME)
_cursor = _connection.cursor()

_cursor.execute(CREATE_TABLE_APPS)
_cursor.execute(CREATE_TABLE_MOVIES)
_cursor.execute(CREATE_TABLE_SONGS)
_cursor.execute(CREATE_TABLE_FILES)
_connection.commit()


def was_file_processed(filename):
	_cursor.execute('SELECT file_name FROM files WHERE file_name=?', (filename,))
	return bool(_cursor.fetchall())


def write_file_processed(filename):
	write('files', [filename])


def write_data(data_obj):
	table_name = TABLE_NAMES.get(data_obj.__class__, None)
	if table_name:
		query = INSERT_FULL_TEMPLATE.format(table_name,
											','.join(data_obj.data.keys()),
											','.join(['?'] * len(data_obj.data.values())))
		try:
			_cursor.execute(query, list(data_obj.data.values()))
		except sqlite3.IntegrityError:
			print('Duplicate detected for given values: ', data_obj.__class__.__name__,
					list(data_obj.data.values()))


def write(db_name, values):
	query = INSERT_TEMPLATE.format(db_name, ','.join(['?'] * len(values)))
	try:
		_cursor.execute(query, values)
	except sqlite3.IntegrityError:
		print('Duplicate detected for given values: ', values)


def finish_transactions():
	_connection.commit()
