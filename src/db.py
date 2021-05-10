import os
import sqlite3

from src import settings
from src.data import App, Song, Movie

# SQL Insertion template
INSERT = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'

# Names of the tables in the database
TABLE_NAMES = {
	App: 'apps',
	Song: 'songs',
	Movie: 'movies',
}

# Names of columns in database tables
# Sorting needed for proper writing
TABLE_COLS = {
	App: sorted(['name', 'genre', 'rating', 'version', 'size_bytes', 'is_awesome']),
	Song: sorted(['artist_name', 'title', 'year', 'release', 'ingestion_time']),
	Movie: sorted(['original_title', 'original_language', 'budget', 'is_adult',
					'release_date', 'original_title_normalized']),
}

# For every table, get INSERT query with column names
INSERT_QUERIES = {
	obj_class: INSERT.format(TABLE_NAMES[obj_class],
							','.join(fields),				# INTO _ (..,..)
							','.join(['?'] * len(fields)))  # VALUES (?,...)
	for (obj_class, fields) in TABLE_COLS.items()
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

DB_NAME = settings.PROFILE.get('DATABASE_NAME')
if not DB_NAME:
	raise KeyError('ImproperlyConfigured: DATABASE_NAME should be set')

DB_PATH = os.path.abspath(os.path.join(__file__, '..\\..\\' + DB_NAME))
_connection = sqlite3.connect(DB_PATH)

_connection.execute(CREATE_TABLE_APPS)
_connection.execute(CREATE_TABLE_MOVIES)
_connection.execute(CREATE_TABLE_SONGS)
_connection.commit()


def write_objects(data_objects: list):
	"""
	Writes given objects (instances of data.DataType) to the database

	:param data_objects: objects to write
	"""
	groups = _group_objects(data_objects)
	# For every class in group, write their objects
	for obj_class in groups.keys():
		query = INSERT_QUERIES.get(obj_class, None)
		if query:
			_connection.executemany(query, groups[obj_class])


def _group_objects(objects: list) -> dict:
	"""
	Groups given objects (instances of data.DataType) by classes

	:param objects: objects to group
	:return: dictionary: {class: [objects values]}
	"""
	classes = set(map(lambda x: x.__class__, objects))
	# For every class, get a list of items and then theirs values
	return {cls: list(map(lambda y: y.values,
						filter(lambda x: x.__class__ == cls, objects)))
			for cls in classes}


def commit():
	"""
	Applies database changes
	"""
	_connection.commit()
