#!/usr/bin/env python

from wsgiref.simple_server import make_server
import mimetypes
import os

config_filename  = 'Config.txt'
source_directory = 'Resources'

def get_contents_of_file(filepath):
  with open(filepath) as in_file:
    return in_file.read()

def get_files_dict(directory):
  return {filename : get_contents_of_file(os.path.join(directory, filename))
          for filename in os.listdir(directory)}

print('Welcome to Servr - desktop edition!')
with open(config_filename, 'a+') as in_file:
  pass  # if config file does not already exist, create one
config = get_contents_of_file(config_filename).split('\n')
do_auto_start = config[0].lower() if config else 'n'
if do_auto_start == 'y':
  print("Getting data from {}...".format(config_filename))
  filename, address, port = config[1:4]
else:
  filename = raw_input("Enter homepage HTML file name including extension:").strip()
  address = raw_input("Enter this device's private IP address:").strip()
  port = raw_input("Enter an unused port:").strip()
  if filename and address and port:
    msg = "Save these values into {}? (No)".format(config_filename)
    save_to_cfg = (raw_input(msg).strip().lower() or 'n')[0]
    if save_to_cfg == 'y':
      with open(config_filename, 'w') as out_file:
        out_file.write('\n'.join(['y', filename, address, port, '']))
htmlData = get_contents_of_file(os.path.join(source_directory, filename))
files_dict = get_files_dict(source_directory)

def host(environ, start_response):
  mimeType = 'text/html'
  status = '200 OK'
  path_info = environ.get('PATH_INFO', None)
  if path_info in (None, '/', '/home', '/index.html'):
    dataToReturn = htmlData
  else:
    path_info = path_info.strip('/')
    dataToReturn = files_dict.get(path_info, None)
    if dataToReturn:
      mimeType = mimetypes.guess_type(path_info)[0]
    else:
      dataToReturn = status = '404 Not Found'
  headers = [('Content-type', mimeType)]
  start_response(status, headers)
  return [dataToReturn]

webServer = make_server(address, int(port), host)
print('Serving at url: http://{}:{}'.format(address, port))
webServer.serve_forever()
