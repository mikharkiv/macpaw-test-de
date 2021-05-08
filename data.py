import re
from datetime import datetime
from abc import abstractmethod, ABC


class DataType(ABC):
	fields = {}
	__data = {}
	__is_valid = False

	def __init__(self, **kwargs):
		self.__data = kwargs
		self.__validate()
		self.__process()

	def __validate(self):
		for (name, typ) in self.fields.items():
			if type(self.__data.get(name, None)) != type:
				self.__is_valid = False
				return
		self.__is_valid = True

	@abstractmethod
	def __process(self):
		pass

	@property
	def is_valid(self):
		return self.__is_valid

	@property
	def data(self):
		return list(self.__data.values())


class Song(DataType):
	fields = {
		'artist_name': 'str',
		'title': 'str',
		'year': 'int',
		'release': 'str',
	}

	def __process(self):
		self.__data['ingestion_time'] = datetime.now()


class Movie(DataType):
	fields = {
		'original_title': 'str',
		'original_language': 'str',
		'budget': 'int',
		'is_adult': 'bool',
		'release_date': 'str',
	}

	def __process(self):
		self.__normalize_title()
		parsed_date = datetime.strptime(self.__data['release_date'], '%Y-%m-%d')
		self.__data['release_date'] = parsed_date

	def __normalize_title(self):
		lowered_title = self.__data['original_title'].lower()
		underscored_title = re.sub(r' +', '_', lowered_title)
		clean_title = re.sub(r'\W', '', underscored_title)
		self.__data['original_title'] = clean_title


class App(DataType):
	fields = {
		'name': 'str',
		'genre': 'str',
		'rating': 'float',
		'version': 'str',
		'size_bytes': 'int',
	}

	def __process(self):
		self.__data['is_awesome'] = len(self.__data['name']) > 8
