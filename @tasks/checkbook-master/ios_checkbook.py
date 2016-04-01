import sqlite3
# Include the Dropbox SDK libraries
from dropbox import client, rest, session
import webbrowser
from datetime import date
from sys import argv

script, name, amount = argv

amount = amount[1:]
today = date.today().strftime('%Y-%m-%d')
# Get your app key and secret from the Dropbox developer website
APP_KEY = <INSERT ACCESS KEY>
APP_SECRET = <INSERT SECRET>

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

url = sess.build_authorize_url(request_token)

#Make the user sign in and authorize this token
print "url:", url
print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
webbrowser.open(url)
raw_input()
# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)

####BEGIN CHECKBOOK CODE
###replace checkbook.test.db with you db

client = client.DropboxClient(sess)

f = client.get_file('/checkbook.test.db').read()
with open('checkbook.test.db','r+') as file:
   file.write(f)

transaction = {}
conn = sqlite3.connect('checkbook.test.db')
c = conn.cursor()
   
def deposit(name, amount):   
   c.execute("INSERT INTO deposits (NAME, AMOUNT, DATE) VALUES ('{}', {}, '{}')".format(name, float(amount.strip()[1:-1]), today))
   conn.commit()
   print('deposit successful')

def withdraw(name, amount):
   c.execute("INSERT INTO withdrawals (NAME, AMOUNT, DATE) VALUES ('{}', {}, '{}')".format(name, float(amount), today))
   conn.commit() 
   print('withdrawal successful')
 
withdrawals_val = 0   
deposits_val = 0

def get_vals(val,table):
      c.execute("SELECT amount FROM {}".format(table))
      for row in c.fetchall():
         val += (float(str(row)[1:-2]))
      return (val)

if amount.startswith('('):
   deposit(name, amount)
else:
   withdraw(name, amount)

print('balance = {}'.format(get_vals(deposits_val,'deposits') -get_vals(withdrawals_val,'withdrawals')))
   
with open('checkbook.test.db', 'r+') as f:
   client.put_file('/checkbook.test.db', f,True)
