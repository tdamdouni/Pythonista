# coding: utf-8

# https://forum.omz-software.com/topic/578/opening-word-documents-in-pythonista/8

from bottle import get, post, request, run

import webbrowser

import console

import os

@get('/start')

def start():
	f = 'test.docx'
	outfile_path = os.path.abspath(f)
	console.quicklook(outfile_path)
	return 'Success!'
webbrowser.open('http://localhost:8080/start')

run(host='localhost', port=8080)

