# coding: utf-8

# https://gist.githubusercontent.com/henryaukc/6fd00b8baee4c069a2b44e574829469f/raw/8424c66008b5105be10abcaf42804a370541f1af/DownloadFacebookVideo.py

# https://forum.omz-software.com/topic/3636/how-to-login-facebook-with-request-module-for-further-access

import webbrowser, os, requests, re, bs4
import appex
import console
import dialogs

data_dir = os.path.join(os.path.abspath('.'),'Videos')

if not os.path.isdir (data_dir):
	#print(data_dir)
	os.makedirs(data_dir)

os.chdir(data_dir)
#ßprint(os.path.abspath('.'))

def download_file(url, tmpfile=None):
	if not tmpfile:
		local_filename = url.split('/')[-1]
	else:
		local_filename = tmpfile
		with open(local_filename, 'wb') as f:
			r = requests.get(url, stream=True)
			total_length = r.headers.get('content-length')
			if not total_length:
				f.write(r.content)
			else:
				dl = 0
				total_length = float(total_length)
				for chunk in r.iter_content(1024):
					dl += len(chunk)
					f.write(chunk)
	return local_filename

def DownloadFile(url, filename):
	res = requests.get(url)
	
	try:
		res.raise_for_status()
	except Exception as exc:
		print('There was a problem: %s' % (exc))

	with open(filename, "wb") as code:
		code.write(res.content)

	
''''	playFile = open(filename, 'wb')	
	for chunk in res.iter_content(100000):
		playFile.write(chunk)
		print('Writing 100000 bytes')
		
		playFile.close()
'''		
	

def OpenURL(url):
	res = requests.get(url)	
	res.encoding = 'utf-8' # 中文顯示必用 
	try:
		res.raise_for_status()
	except Exception as exc:
		print('There was a problem: %s' % (exc))
	return res		


def DownloadFacebookVideo(url):
	title_length = 50
	r = OpenURL(url)			

	doc = r.text 
	#print(doc)
	soup = bs4.BeautifulSoup(doc, 'html5lib') 
	#elements = soup.find_all('div', attrs={class: '_5pbx userContent'})

	elements = soup.find_all(class_ = '_5pcq')
	#print('Elements:' + str(elements))

	video_list = []
	title_list = []
	for i in range(len(elements)): # Search all the posts which contains video
		#print (str(elements[i]['href']))
		r1 = (re.search(r'videos/(\d+)/', str(elements[i]['href'])))
		if not r1:
		#	Skipped all posts without video
			continue
		video_id = r1.group(1)
		#print (video_id)
		x = elements[i].findNext('p')
		t = x.getText() # Get the text of the post which contains video
		if len(t) > title_length:
				t = t[0:title_length] + '...'
	
		temp_dict = {'text': t, 'video_id': video_id, 'hd_src': None, 'sd_src': None, 'sd_src_no_ratelimit':None, 'hd_src_no_ratelimit': None}
		video_list.append(temp_dict)
		title_list.append(t)

	#print(len(video_list))
	for i in range(len(video_list)):
		video_id = video_list[i]['video_id']
		#print ('video_id: ' + video_id)
		patt = r'\[\{"is_hds":(?:false|true),"video_id":"' + video_id +  '".*?"sd_src_no_ratelimit":"(.*?)".*?"hd_src_no_ratelimit":"(.*?)".*?"hd_src":"(.*?)".*?"sd_src":"(.*?)".*?\}\]'
		r2 = re.search(patt, doc)
		
		if r2.group(1) != '':
			video_list[i]['sd_src_no_ratelimit'] = r2.group(1).replace('\/','/')
		if r2.group(2) != '':
			video_list[i]['hd_src_no_ratelimit'] = r2.group(2).replace('\/','/')
		if r2.group(3) != '':
			video_list[i]['hd_src'] = r2.group(3).replace('\/','/')
		if r2.group(4) != '':
			video_list[i]['sd_src'] = r2.group(4).replace('\/','/')
		
#	print(video_list)	
	for i in range(len(video_list)):
		t = video_list[i]['text']
		if video_list[i]['hd_src'] != None:
			url = video_list[i]['hd_src']
			video_quality = 'hd_src'
		elif video_list[i]['hd_src_no_ratelimit'] != None:
			url = video_list[i]['hd_src_no_ratelimit']
			video_quality = 'hd_src_no_ratelimit'		
		elif video_list[i]['sd_src_no_ratelimit'] != None:
			url = video_list[i]['sd_src_no_ratelimit']
			video_quality = 'sd_src_no_ratelimit'		
		elif video_list[i]['sd_src'] != None:
			url = video_list[i]['sd_src']
			video_quality = 'sd_src'		
		else:
			video_quality = None
			print('No video found!!')
		
	item = dialogs.list_dialog('Pick', title_list)
	if item != None:
		for i, text in enumerate(title_list):
			if item == text:
				vq_list = {}
				if video_list[i]['hd_src'] != None:
					vq_list['hd_src'] = video_list[i]['hd_src']
				
				if video_list[i]['hd_src_no_ratelimit'] != None:
					vq_list['hd_src_no_ratelimit'] = video_list[i]['hd_src_no_ratelimit']
					
				if video_list[i]['sd_src'] != None:
					vq_list['sd_src'] = video_list[i]['sd_src']					

				if video_list[i]['sd_src_no_ratelimit'] != None:
					vq_list['sd_src_no_ratelimit'] = video_list[i]['sd_src_no_ratelimit']
						
				
				video_quality = dialogs.list_dialog('Pick the Video Quality', sorted(vq_list.keys()))
				if video_quality != None:
					fname = (video_list[i]['text'])[0:20] + '(' + video_quality +').mp4'
					#console.set_color(0,0,255)
					#print('URL:' + vq_list[video_quality])
					print ('Downloading ""' + fname + '"...')
					#console.hud_alert('Downloading ""' + fname + '"...')
			
					download_file(vq_list[video_quality], fname)
					#DownloadFile(vq_list[video_quality], fname) 					#(not working in some cases)
					console.hud_alert('Done!')
					return fname
				else:
					return None
	else:
		return None
		
def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	
	url = appex.get_url()
	if not url:
		print('No input URL found.')
		return 

	#url = 'https://www.facebook.com/Spurs/?ref=ts&fref=ts'
	
	fname = DownloadFacebookVideo(url)
	if fname != None:
		console.quicklook(fname)
		os.remove(fname)
	
if __name__ == '__main__':
	main()
