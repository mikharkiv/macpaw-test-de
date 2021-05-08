import sqlite3

import settings

CREATE_TABLE_SONGS = '''
CREATE TABLE IF NOT EXISTS songs (
	artist_name TEXT NOT NULL,
	title TEXT NOT NULL,
	year INTEGER NOT NULL,
	`release` TEXT NOT NULL,
	ingestion_time INTEGER NOT NULL,
	PRIMARY KEY (title)
);'''

CREATE_TABLE_MOVIES = '''
CREATE TABLE IF NOT EXISTS movies (
	original_title TEXT NOT NULL,
	original_language TEXT NOT NULL,
	budget INTEGER NOT NULL,
	is_adult INTEGER NOT NULL,
	release_date INTEGER NOT NULL,
	original_title_normalized TEXT NOT NULL,
	PRIMARY KEY (original_title_normalized)
);'''

CREATE_TABLE_APPS = '''
CREATE TABLE IF NOT EXISTS apps (
	name TEXT NOT NULL,
	genre TEXT NOT NULL,
	rating REAL NOT NULL,
	version TEXT NOT NULL,
	size_bytes INTEGER NOT NULL,
	is_awesome INTEGER NOT NULL,
	PRIMARY KEY (name)
);'''

INSERT_TEMPLATE = f'INSERT INTO {0} VALUES (?)'

DB_NAME = settings.dev.get('DATABASE_NAME', None)

if not DB_NAME:
	raise KeyError('Database name should be specified')

__connection = sqlite3.connect(DB_NAME)
__cursor = __connection.cursor()

__cursor.execute(CREATE_TABLE_APPS)
__cursor.execute(CREATE_TABLE_MOVIES)
__cursor.execute(CREATE_TABLE_SONGS)
__connection.commit()


def write(db_name, values):
	query = INSERT_TEMPLATE.format(db_name)
	__cursor.executemany(query, values)
	__connection.commit()
