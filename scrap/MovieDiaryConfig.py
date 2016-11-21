# coding: utf-8

# https://gist.github.com/philgruneich/2c41b94ab6b8b6d371b0

# https://onetapless.com/update-new-movie-diary

import dialogs
import keychain
import console
import cPickle
from urllib import quote, unquote

class NoConfigError (Exception): pass
class MissingConfigError (Exception): pass

try:
	moviediary_config = cPickle.loads(keychain.get_password('Movie Diary', 'Config'))
	if moviediary_config == None:
		raise MissingConfigError('There\'s no config for the Movie Diary to edit. Run the Movie Diary to generate one.' )
	else:
		moviediary_edit = dialogs.form_dialog(title='Movie Diary Configuration', sections=[('MovieDB', [{'type': 'text', 'key': 'moviedb_api', 'value': moviediary_config['moviedb_api'], 'title': 'MovieDB API Token'}]), ('Airtable', [{'type': 'text', 'key': 'airtable_api', 'value': moviediary_config['airtable_api'], 'title': 'Airtable API Key'}, {'type': 'text', 'key': 'airtable_db', 'value': moviediary_config['airtable_db'], 'title': 'Airtable database ID'},{'type': 'text', 'key': 'airtable_table', 'value': unquote(moviediary_config['airtable_table']), 'title': 'Airtable table name'}]), ('Custom', [{'type': 'switch', 'key': 'set_date_manually', 'value': moviediary_config['set_date_manually'], 'title': 'Set date manually'},{'type': 'switch', 'key': 'add_time_to_date', 'value': moviediary_config['add_time_to_date'], 'title': 'Add time to date'}]),('Extra Fields', [{'type': 'switch', 'key': 'directors_field', 'value': moviediary_config['directors_field'], 'title': 'Directors'},{'type': 'switch', 'key': 'genres_field', 'value': moviediary_config['genres_field'], 'title': 'Genres'},{'type': 'switch', 'key': 'runtime_field', 'value': moviediary_config['runtime_field'], 'title': 'Runtime'},{'type': 'switch', 'key': 'cast_field', 'value': moviediary_config['cast_field'], 'title': 'Cast'}, {'type': 'switch', 'key': 'imdb_field', 'value': moviediary_config['imdb_field'], 'title': 'IMDB URL'}])])
		
		if moviediary_edit != None:
			if moviediary_edit['moviedb_api'] == '':
				moviedb_api = console.input_alert('Insert your TMDB API key', '', '84cef43ccf02b1ba6093c9694ed671c9')
				if moviedb_api == None:
					raise MissingConfigError('You need a valid MovieDB API key')
				else:
					moviediary_edit['moviedb_api'] = moviedb_api

			if moviediary_edit['airtable_api'] == '':
				airtable_api = console.input_alert('Insert your Airtable API key')
				if airtable_api == None:
					raise MissingConfigError('You need a valid Airtable API key')
				else:
					moviediary_edit['airtable_api'] = airtable_api

			if moviediary_edit['airtable_db'] == '':
				airtable_db = console.input_alert('Insert your Airtable database ID')
				if airtable_db == None:
					raise MissingConfigError('You need the ID of your database')
				else:
					moviediary_edit['airtable_db'] = airtable_db

			if moviediary_edit['airtable_table'] == '':
				airtable_table = console.input_alert('Insert the name of yout Airtable table', '', 'Table 1')
				if airtable_table == None:
					raise MissingConfigError('You must insert the name of the table in your database.')
				else:
					moviediary_edit['airtable_table'] = quote(airtable_table)
			
			keychain.set_password('Movie Diary', 'Config', cPickle.dumps(moviediary_edit))
			console.hud_alert('Movie Diary Configuration Successfully Edited')
except NoConfigError as e:
	console.alert('No Config', e)
except MissingConfigError as e:
	console.alert('Missing Config Field', e)
