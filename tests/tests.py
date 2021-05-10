import unittest

from src.data import App, Movie, Song


class DataTypesTest(unittest.TestCase):
	def test_app(self):
		app = App()
		app.setup()
		self.assertFalse(app.is_valid)

		app = App()
		app.setup(name=1, genre=2, rating='a', version='1', size_bytes=0)
		self.assertFalse(app.is_valid)

		app = App()
		app.setup(name='n', genre='g', rating=0., version='1', size_bytes=100)
		self.assertTrue(app.is_valid)
		self.assertTrue(app.data['is_awesome'])

	def test_movie(self):
		movie = Movie()
		movie.setup(original_title='a', original_language='ua', budget=0,
					is_adult=False, release_date='01-21-2001')
		self.assertTrue(movie.is_valid)

		movie = Movie()
		movie.setup(original_title=0, original_language='ua', budget=0,
					is_adult=False, release_date='01-21-2001')
		self.assertFalse(movie.is_valid)

		movie = Movie()
		movie.setup(original_title='Hello !@#world!!', original_language='ua', budget=0,
					is_adult=False, release_date='01-21-2001')
		self.assertTrue(movie.is_valid)
		self.assertEqual('hello_world', movie.data['original_title_normalized'])

	def test_song(self):
		song = Song()
		song.setup(artist_name='a', title='y', year=2020, release='s')
		self.assertTrue(song.is_valid)

		song = Song()
		song.setup(artist_name='a', title='y', year='2020', release='s')
		self.assertFalse(song.is_valid)
