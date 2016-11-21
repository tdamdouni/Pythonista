# coding: utf-8

# https://gist.github.com/philgruneich/72f2fb734dcaf404cf36

# https://onetapless.com/update-new-movie-diary

import requests
import json
import appex
import dialogs
import re
import datetime
import keychain
import console
import sys
import cPickle
from urllib import quote, unquote

class NoResultsError (Exception): pass
class NoMoviePickError (Exception): pass
class NoRatingError (Exception): pass
class TmdbConnectionError (Exception): pass
class AirtableConnectionError (Exception): pass
class MissingConfigError (Exception): pass
class InvalidColumnError (Exception): pass
class NoDatabaseError (Exception): pass
class NoApiKeyError (Exception): pass
class NoTableError (Exception): pass
class ProbablyBadLoginError (Exception): pass

class MovieDiary():

	def __init__(self):
		config = keychain.get_password('Movie Diary', 'Config')
		
		if config == None:
			
			moviedb_api = keychain.get_password('MovieDB', 'API')
			airtable_api = keychain.get_password('Airtable', 'API')
			airtable_db = keychain.get_password('Airtable', 'Movie Diary')
			airtable_table = keychain.get_password('Airtable', 'Movie Diary Table')
			
			if airtable_api == None or airtable_db == None or airtable_table == None:
				airtable_api, airtable_db, airtable_table = self.getairtable(airtable_api, airtable_db, airtable_table)
			
			config = dialogs.form_dialog(title='Movie Diary Configuration', sections=[('MovieDB', [{'type': 'text', 'key': 'moviedb_api', 'value': moviedb_api if moviedb_api is not None else '84cef43ccf02b1ba6093c9694ed671c9', 'title': 'MovieDB API Token'}]), ('Airtable', [{'type': 'text', 'key': 'airtable_api', 'value': airtable_api, 'title': 'Airtable API Key'}, {'type': 'text', 'key': 'airtable_db', 'value': airtable_db, 'title': 'Airtable database ID'}, {'type': 'text', 'key': 'airtable_table', 'value': airtable_table if airtable_table is not None else 'Table 1', 'title': 'Airtable table name'}]), ('Custom', [{'type': 'switch', 'key': 'set_date_manually', 'value': False, 'title': 'Set date manually'}, {'type': 'switch', 'key': 'add_time_to_date', 'value': False, 'title': 'Add time to date'}]),('Extra Fields', [{'type': 'switch', 'key': 'directors_field', 'value': True, 'title': 'Directors'}, {'type': 'switch', 'key': 'genres_field', 'value': False, 'title': 'Genres'}, {'type': 'switch', 'key': 'runtime_field', 'value': False, 'title': 'Runtime'}, {'type': 'switch', 'key': 'cast_field', 'value': False, 'title': 'Cast'}, {'type': 'switch', 'key': 'imdb_field', 'value': False, 'title': 'IMDB URL'}]),('Fields', [{'type':'text', 'key': 'title_field_name', 'value': 'Title', 'title': 'Title'}, {'type':'text', 'key': 'overview_field_name', 'value': 'Overview', 'title': 'Overview'}, {'type':'text', 'key': 'rating_field_name', 'value': 'Rating', 'title': 'Rating'}, {'type':'text', 'key': 'date_field_name', 'value': 'Date', 'title': 'Date'}, {'type':'text', 'key': 'directors_field_name', 'value': 'Directors', 'title': 'Directors'}, {'type':'text', 'key': 'poster_field_name', 'value': 'Poster', 'title': 'Poster'}, {'type':'text', 'key': 'year_field_name', 'value': 'Year', 'title': 'Year'}, {'type':'text', 'key': 'genres_field_name', 'value': 'Genres', 'title': 'Genres'}, {'type':'text', 'key': 'cast_field_name', 'value': 'Cast', 'title': 'Cast'}, {'type':'text', 'key': 'runtime_field_name', 'value': 'Runtime', 'title': 'Runtime'}, {'type':'text', 'key': 'imdb_field_name', 'value': 'IMDB', 'title': 'IMDB URL'}])])
			
			if config == None:
				raise MissingConfigError('You must setup and confirm the Movie Diary configuration before continuing.')
			else:
				config['moviedb_api'] = self.validate_config(config['moviedb_api'], 'Insert your TMDB API key', 'You need a valid MovieDB API key', '84cef43ccf02b1ba6093c9694ed671c9')
				config['airtable_api'] = self.validate_config(config['airtable_api'], 'Insert your Airtable API key', 'You need a valid Airtable API key')
				config['airtable_db'] = self.validate_config(config['airtable_db'], 'Insert your Airtable database ID', 'You need the ID of your database')
				config['airtable_table'] = self.validate_config(config['airtable_table'], 'Insert the name of yout Airtable table', 'You must insert the name of the table in your database.', 'Table 1', True)
				
				keychain.set_password('Movie Diary', 'Config', cPickle.dumps(config))
		else:
			config = cPickle.loads(config)

		self.moviedb_api = config.get('moviedb_api', '')
		self.airtable_api = config.get('airtable_api', '')
		self.airtable_db = config.get('airtable_db', '')
		self.airtable_table = config.get('airtable_table', '')
		self.set_date_manually = config.get('set_date_manually', '')
		self.add_time_to_date = config.get('add_time_to_date', '')
		self.directors_field = config.get('directors_field', '')
		self.genres_field = config.get('genres_field', '')
		self.runtime_field = config.get('runtime_field', '')
		self.cast_field = config.get('cast_field', '')
		self.imdb_field = config.get('imdb_field', '')
		self.title_field_name = config.get('title_field_name', 'Title')
		self.overview_field_name = config.get('overview_field_name', 'Overview')
		self.rating_field_name = config.get('rating_field_name', 'Rating')
		self.date_field_name = config.get('date_field_name', 'Date')
		self.directors_field_name = config.get('directors_field_name', 'Directors')
		self.poster_field_name = config.get('poster_field_name', 'Poster')
		self.year_field_name = config.get('year_field_name', 'Year')
		self.genres_field_name = config.get('genres_field_name', 'Genres')
		self.cast_field_name = config.get('cast_field_name', 'Cast')
		self.runtime_field_name = config.get('runtime_field_name', 'Runtime')
		self.imdb_field_name = config.get('imdb_field_name', 'IMDB')

	@staticmethod
	def getairtable(api, db, table):
		import mechanize
		import cookielib
		from bs4 import BeautifulSoup as bs
		
		browser = mechanize.Browser()
		jar = cookielib.LWPCookieJar()
		browser.set_cookiejar(jar)
		browser.open('https://airtable.com/login?continue=/api')

		auth = dialogs.login_alert('Your Airtable login and password', 'We need it to select a database. Your credentials won\'t be stored.')
		
		browser.select_form(nr=0)
		browser.form['email'] = auth[0]
		browser.form['password'] = auth[1]
		browser.submit()
		resp = browser.open('https://airtable.com/auth/redirectAfterSuccessfulLogin?url=%2Fapi')
		
		if db != None:
			db_key = db
		else:
			soup = bs(resp.read())
			apps = soup.find(id='apps')
			if apps != None:
				db_strings = [app.text for app in apps.find_all('span', class_='name')]
				db_chosen = db_strings[0] if len(db_strings) == 1 else dialogs.list_dialog('Choose a database', db_strings)
				
				if db_chosen != None:
					db_key = [li['menuitemvalue'] for li in apps.find_all('li') if li.span.string == db_chosen][0]
				else:
					# Didn't choose a database
					raise NoDatabaseError()
			else:
				# No apps, so it failed to login. Probably wrong password.
				raise ProbablyBadLoginError()
		
		if api == None or table == None:
			docs = browser.open('https://airtable.com/%s/api/docs' % db_key)
			docsoup = bs(docs.read())
			if api == None:
				api_key_div = docsoup.body.find(lambda tag : tag.has_attr('data-api-key'))
				
				if api_key_div != None:
					api_key = api_key_div['data-api-key']
					if api_key == '':
						# No API key
						raise NoApiKeyError()
				else:
					# No documentation, probably failed login and wrong password.
					raise ProbablyBadLoginError()
			else:
				api_key = api

			if table == None:
				script = docsoup.find('script').text
				pattern = r'({.*);'	
				match = re.search(pattern, script)
				if match != None:
					tables = [table['name'] for table in json.loads(match.group(1))['tables']]
					table_key = tables[0] if len(tables) == 1 else dialogs.list_dialog('Choose a table', tables)
					
					if table_key == None:
						# Didn't choose a table
						raise NoTableError()
				else:
					# Couldn't find any table, probably a failed login.
					raise ProbablyBadLoginError()
			else:
				table_key = table
		
		return api_key, db_key, table_key
			
	@staticmethod
	def validate_config(key, message='', error='', default='', quoted=False):
		if key == '':
			item = console.input_alert(message, '', default)
			if item == None:
				raise MissingConfigError(error)
			else:
				return quote(item) if quoted else item
		else:
			return key

	@staticmethod
	def getyear(d, raw=False):
		if d is None or d == '':
			return ''
		elif raw:
			return str(d[:4])
		else:
			return ' (%s)' % d[:4]

	@staticmethod
	def getgenres(genres):
		return '/'.join([genre['name'] for genre in genres])

	def getcredits(self, url, params):
		req = requests.get('%s/credits' % (url), params=params)

		if req.status_code == 200:
			res = json.loads(req.text)
			directors = []
			cast = []
			
			if self.directors_field:
				directors = ', '.join([director['name'] for director in res['crew'] if director['job'] == 'Director'])
			if self.cast_field:
				cast = ', '.join([res['cast'][i]['name'] for i in range(min(5, len(res['cast'])))])
			
			return (cast, directors)
		else:
			raise TmdbConnectionError(req.text)

	def getdate(self):
		if self.set_date_manually and self.add_time_to_date:
			return dialogs.datetime_dialog().isoformat()
		elif self.set_date_manually:
			return dialogs.date_dialog().isoformat()
		elif self.add_time_to_date:
			return datetime.datetime.now().isoformat()
		else:
			return datetime.datetime.now().date().isoformat()

	def journal(self, data):
		headers = {
			'Authorization': 'Bearer %s' % self.airtable_api,
			'Content-type': 'application/json'
		}

		req = requests.post('https://api.airtable.com/v0/{0}/{1}'.format(self.airtable_db, self.airtable_table), headers=headers, data=json.dumps({'fields': data}))

		if req.status_code == 200:
			console.hud_alert('Added movie', 'success')
		elif req.status_code == 422:
			raise InvalidColumnError(json.loads(req.text))
		else:
			raise AirtableConnectionError(req.text)

	def getmovie(self, url, params):
		req = requests.get(url, params=params)

		if req.status_code == 200:
			res = json.loads(req.text)

			fields = {
				self.overview_field_name: res['overview'],
				self.title_field_name: res['title'],
				self.year_field_name: self.getyear(res['release_date'], True),
				self.date_field_name: self.getdate(),
				self.rating_field_name: dialogs.list_dialog("Rate '{0}'".format(res['title']), ['★★★★★', '★★★★½', '★★★★', '★★★½', '★★★', '★★½', '★★', '★½', '★', '½'])
			}
			
			if self.cast_field or self.directors_field:
				credits = self.getcredits(url, params)
				if self.cast_field:
					fields[self.cast_field_name] = credits[0]
				if self.directors_field:
					fields[self.directors_field_name] = credits[1]
			
			if self.runtime_field:
				fields[self.runtime_field_name] = res['runtime']
			
			if self.imdb_field:
				fields[self.imdb_field_name] = 'http://www.imdb.com/title/%s/' % res['imdb_id']
			
			if self.genres_field:
				fields[self.genres_field_name] = self.getgenres(res['genres'])

			if res['poster_path'] is not None:
				fields[self.poster_field_name] = [{'url': 'https://image.tmdb.org/t/p/original%s' % res['poster_path']}]
			if fields[self.rating_field_name] is not None:
				return self.journal(fields)
			else:
				raise NoRatingError()
		else:
			raise TmdbConnectionError(req.text)

	def edit_config(self):
		config = dialogs.form_dialog(title='Movie Diary Configuration', sections=[('MovieDB', [{'type': 'text', 'key': 'moviedb_api', 'value': self.moviedb_api, 'title': 'MovieDB API Token'}]), ('Airtable', [{'type': 'text', 'key': 'airtable_api', 'value': self.airtable_api, 'title': 'Airtable API Key'}, {'type': 'text', 'key': 'airtable_db', 'value': self.airtable_db, 'title': 'Airtable database ID'}, {'type': 'text', 'key': 'airtable_table', 'value': self.airtable_table, 'title': 'Airtable table name'}]), ('Custom', [{'type': 'switch', 'key': 'set_date_manually', 'value': self.set_date_manually, 'title': 'Set date manually'}, {'type': 'switch', 'key': 'add_time_to_date', 'value': self.add_time_to_date, 'title': 'Add time to date'}]),('Extra Fields', [{'type': 'switch', 'key': 'directors_field', 'value': self.directors_field, 'title': 'Directors'}, {'type': 'switch', 'key': 'genres_field', 'value': self.genres_field, 'title': 'Genres'}, {'type': 'switch', 'key': 'runtime_field', 'value': self.runtime_field, 'title': 'Runtime'}, {'type': 'switch', 'key': 'cast_field', 'value': self.cast_field, 'title': 'Cast'}, {'type': 'switch', 'key': 'imdb_field', 'value': self.imdb_field, 'title': 'IMDB URL'}]),('Fields', [{'type':'text', 'key': 'title_field_name', 'value': self.title_field_name, 'title': 'Title'}, {'type':'text', 'key': 'overview_field_name', 'value': self.overview_field_name, 'title': 'Overview'}, {'type':'text', 'key': 'rating_field_name', 'value': self.rating_field_name, 'title': 'Rating'}, {'type':'text', 'key': 'date_field_name', 'value': self.date_field_name, 'title': 'Date'}, {'type':'text', 'key': 'directors_field_name', 'value': self.directors_field_name, 'title': 'Directors'}, {'type':'text', 'key': 'poster_field_name', 'value': self.poster_field_name, 'title': 'Poster'}, {'type':'text', 'key': 'year_field_name', 'value': self.year_field_name, 'title': 'Year'}, {'type':'text', 'key': 'genres_field_name', 'value': self.genres_field_name, 'title': 'Genres'}, {'type':'text', 'key': 'cast_field_name', 'value': self.cast_field_name, 'title': 'Cast'}, {'type':'text', 'key': 'runtime_field_name', 'value': self.runtime_field_name, 'title': 'Runtime'}, {'type':'text', 'key': 'imdb_field_name', 'value': self.imdb_field_name, 'title': 'IMDB URL'}]), ('Serious Stuff', [{'type': 'switch', 'key': 'reset_config', 'title': 'Reset Configuration', 'value': False}])])

		if config != None:
			
			if config['reset_config']:
				reset_confirm = console.alert('Reset Configuration?', 'Are you sure? This will only clean your credentials data and has no relation to your database.', 'Cancel', 'Reset', hide_cancel_button=True)
				
				if reset_confirm == 2:
					keychain.delete_password('Movie Diary', 'Config')
					keychain.delete_password('Airtable', 'API')
					keychain.delete_password('Airtable', 'Movie Diary')
					keychain.delete_password('Airtable', 'Movie Diary Table')
					return console.hud_alert('Movie Diary Configuration Successfully Reset')
				
			config['moviedb_api'] = self.validate_config(config['moviedb_api'], 'Insert your TMDB API key', 'You need a valid MovieDB API key', '84cef43ccf02b1ba6093c9694ed671c9')
			config['airtable_api'] = self.validate_config(config['airtable_api'], 'Insert your Airtable API key', 'You need a valid Airtable API key')
			config['airtable_db'] = self.validate_config(config['airtable_db'], 'Insert your Airtable database ID', 'You need the ID of your database')
			config['airtable_table'] = self.validate_config(config['airtable_table'], 'Insert the name of yout Airtable table', 'You must insert the name of the table in your database.', 'Table 1', True)

			keychain.set_password('Movie Diary', 'Config', cPickle.dumps(config))
			console.hud_alert('Movie Diary Configuration Successfully Edited')
		else:
			raise MissingConfigError('You must setup and confirm the Movie Diary configuration before continuing.')

	def log(self):
		console.show_activity()
		try:
			url_match = re.match(r'^https?://(?:www\.)?imdb\.com/title/(tt\d+)/?', appex.get_url())
			params = {
				'api_key': self.moviedb_api,
				'external_source': 'imdb_id'
			}
			return self.getmovie('https://api.themoviedb.org/3/movie/%s' % (url_match.group(1)), params)
		except TypeError:
			params = {
				'api_key': self.moviedb_api,
				'query': console.input_alert('Search for movie', '', sys.argv[1] if len(sys.argv) > 1 else '')
			}

			if len(params.get('query')) == 0:
				self.edit_config()
			else:
				req = requests.post('https://api.themoviedb.org/3/search/movie', params=params)

				if req.status_code == 200:
					res = json.loads(req.text)

					if res['total_results'] > 1:
						results_map = {e['title'] + self.getyear(e['release_date']) : e for e in res['results']}
						movie_pick = dialogs.list_dialog('Pick a movie', [e['title'] + self.getyear(e['release_date']) for e in res['results']])
						if movie_pick is not None:
							return self.getmovie('https://api.themoviedb.org/3/movie/%s' % (results_map[movie_pick]['id']), {'api_key': self.moviedb_api})
						else:
							raise NoMoviePickError()
					elif res['total_results'] == 1:
						return self.getmovie('https://api.themoviedb.org/3/movie/%s' % (res['results'][0]['id']), {'api_key': self.moviedb_api})
					else:
						raise NoResultsError()
				else:
					raise TmdbConnectionError(req.text)

if __name__ == '__main__':
	md = MovieDiary()
	try:
		md.log()
	except MissingConfigError as e:
		console.alert('Missing configuration', str(e))
	except NoResultsError:
		console.alert('No Results', 'Couldn\'t find any movie matching your query.')
	except AirtableConnectionError as e:
		console.alert('Failed to connect to Airtable', str(e))
	except TmdbConnectionError as e:
		console.alert('Failed to connect to MovieDB', str(e))
	except NoMoviePickError:
		console.alert('No movie selected', 'You gotta pick a movie for the script to work.')
	except NoRatingError:
		console.alert('No rating', 'You gotta rate the movie for the script to work.')
	except InvalidColumnError as e:
		console.alert('Invalid Data', '{0}: {1}'.format(e[0]['error']['type'], e[0]['error']['message']))
	except NoDatabaseError:
		console.alert('No database selected', 'You gotta select a database for the script to work.')
	except NoTableError:
		console.alert('No table selected', 'You gotta select a table for the script to work.')
	except NoApiKeyError:
		console.alert('No API key available', 'You gotta generate an API key at https://airtable.com/account.')
	except ProbablyBadLoginError:
		console.alert('Probably a bad login', 'Something went wrong while crawling for your data. The host, connection or script may have failed, but most probably you used the wrong credentials')
