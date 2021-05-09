import re
from datetime import datetime
from abc import abstractmethod, ABC

import settings

DATE_STORE_FORMAT = settings.dev.get('DATE_STORE_FORMAT', '')


class DataType(ABC):
	fields = {}
	_data = {}
	_is_valid = False

	def setup(self, **kwargs):
		self._data = kwargs
		self._validate()
		if self.is_valid:
			self._process()
		else:
			print('!INVALID!', self._data)

	def _validate(self):
		for (name, field_type) in self.fields.items():
			if type(self._data.get(name, None)) != field_type:
				self._is_valid = False
				return
		self._is_valid = True

	@abstractmethod
	def _process(self):
		pass

	@property
	def is_valid(self):
		return self._is_valid

	@property
	def values(self):
		return list(self._data.values())

	@property
	def data(self):
		return self._data.copy()


class Song(DataType):
	fields = {
		'artist_name': str,
		'title': str,
		'year': int,
		'release': str,
	}

	def _process(self):
		self._data['ingestion_time'] = datetime.now().strftime(DATE_STORE_FORMAT)


class Movie(DataType):
	fields = {
		'original_title': str,
		'original_language': str,
		'budget': int,
		'is_adult': bool,
		'release_date': str,
	}

	def _process(self):
		self._normalize_title()

	def _normalize_title(self):
		lowered_title = self._data['original_title'].lower()
		underscored_title = re.sub(r' +', '_', lowered_title)
		clean_title = re.sub(r'\W', '', underscored_title)
		self._data['original_title_normalized'] = clean_title


class App(DataType):
	fields = {
		'name': str,
		'genre': str,
		'rating': float,
		'version': str,
		'size_bytes': int,
	}

	def _process(self):
		self._data['is_awesome'] = len(self._data['name']) > 8
