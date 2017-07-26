# https://forum.omz-software.com/topic/3879/webapp-debugging

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def hello() -> str:
	return 'Hello world from Flask!'
	
@app.route('/search4', methods=['POST'])
def do_search() -> str:
	return str(search4letters('life, the universe and everything','eiru,!'))
	
@app.route('/entry')
def entry_page() -> 'html':
	return render_template('entry.html', the_title='Welcome to search for letters on the web!')
	
app.run(use_reloader=False,debug=True)

