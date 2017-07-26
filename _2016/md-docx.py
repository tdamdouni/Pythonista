# https://gist.github.com/paultopia/a3e9c31da1d27a8ad9be7bf6b3df84a4

import requests
import appex
url = "http://c.docverter.com/convert"
filename = appex.get_file_path()
with open(filename, 'rb') as f:
	r = requests.post(url, data={'to':'docx','from':'markdown'},files={'input_files[]':f})
if r.ok:
	outfile = filename.rpartition('/')[-1].rpartition('.')[0] + '.docx'
	with open(outfile, 'wb') as o:
		o.write(r.content)
	print("success!" + outfile)
else:
	print('request failed: ' + r.status_code)

