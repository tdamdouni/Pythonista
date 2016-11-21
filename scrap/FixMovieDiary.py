# coding: utf-8

# https://gist.github.com/philgruneich/ad8e62c2b7b7ad1b7a7a

import keychain
import console
from urllib import quote, unquote

keychain.set_password('MovieDB', 'API', console.input_alert('Insert your MovieDB API key', '', keychain.get_password('MovieDB', 'API')))
keychain.set_password('Airtable', 'API', console.input_alert('Insert your Airtable API key', '', keychain.get_password('Airtable', 'API')))
keychain.set_password('Airtable', 'Movie Diary', console.input_alert('Insert your Airtable database ID', '', keychain.get_password('Airtable', 'Movie Diary')))
keychain.set_password('Airtable', 'Movie Diary Table', quote(console.input_alert('Insert the name of your Airtable table', '', unquote(keychain.get_password('Airtable', 'Movie Diary Table')))))

console.hud_alert('Updated configuration.')
