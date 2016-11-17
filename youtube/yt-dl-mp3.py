import youtube_dl


class MyLogger(object):
	def debug(self, msg):
		pass
		
	def warning(self, msg):
		pass
		
	def error(self, msg):
		print(msg)
		
		
def my_hook(d):
	if d['status'] == 'finished':
		print('Done downloading, now converting ...')
		
		
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download(['https://youtu.be/9KPBuSHrAyY'])

