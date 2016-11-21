# coding: utf-8

# https://twitter.com/scrubbsMe/status/692190549034561536

from flask import Flask
app = Flask(__name__)

@app.route('/')

def hello_world():
	return 'Hello World in Pythonista ob iOS 9 on iPhone 6+'


if __name__ == '__main__':
	app.run()