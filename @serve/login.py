# coding: utf-8

# https://github.com/tchich/pythonista/blob/master/login.py


from bottle import get, post, request, run # or route
import webbrowser
@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
def check_login(username,password):
	if(username=='admin' and password=='admin'):
		return True 
	return False 
	
webbrowser.open('http://localhost:8080/login')
run(host='localhost', port=8080)