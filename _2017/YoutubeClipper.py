from __future__ import print_function
# https://gist.github.com/allanon2/6239859

import urllib2, urlparse, sys, webbrowser, clipboard, console
 
itags = {'45': 'webm_720p',
         '44': 'webm_480p',
         '43': 'webm_360p',
         '38': 'mp4_3072p',
         '37': 'mp4_1080p',
         '36': 'phone_mp4_240p',
         '35': 'flv_480p',
         '34': 'flv_360p',
         '22': 'mp4_720p',
         '18': 'mp4_360p',
         '17': 'phone_mp4_144p',
          '5': 'flv_240p'}
 
order_preference = ['38', '37', '22', '18']
 
def main():
    v_id = None
    first_pick=None
    link=clipboard.get()
    #link='http://www.youtube.com/watch?v=TE0n_5qPmRM'
    
    if (len(link) > 0):
        try:
            v_id = urlparse.parse_qs(link.split('?')[1])['v'][0]
        except Exception:
            v_id = None
    if not v_id:
        print(repr(link))
        return
    config = urllib2.urlopen('http://www.youtube.com/get_video_info?&video_id=%s&el=detailpage&ps=default&eurl=&gl=US&hl=en' % v_id).read()
    config = urlparse.parse_qs(config)
    formats = [urlparse.parse_qs(x) for x in config['url_encoded_fmt_stream_map'][0].split(',')]
    filtered_formats = dict([(x.get('itag', [0])[0], x) for x in formats if x.get('itag', [0])[0] in order_preference])
    sorted_formats   = [filtered_formats[x] for x in order_preference if filtered_formats.has_key(x)]
    #print(sorted_formats)
    options=[]
    for f in sorted_formats:
    	itag=f['itag'][0]
    	desc=itags[itag]
    	options.append(desc)
   
    if len(options)	< 3:
    	options.append('')
    	
    if (options[2]==''):
    	choice = console.alert('Video selection', 'Video Quality?', options[0], options[1])
    else:
    	choice = console.alert('Video selection', 'Video Quality?', options[0], options[1],options[2])

    first_pick=sorted_formats[choice-1]
  		
  	
	
    download_url = first_pick['url'][0]
    if first_pick.has_key('sig'):
        download_url += ('&signature=' + first_pick['sig'][0])
    download_url = download_url.replace('http://', 'iDownloads://')
    webbrowser.open(download_url)
 
if __name__ == '__main__':
    main()
 
# Bookmarklet:
# javascript:window.location='pythonista://YoutubeDL?action=run&argv='+encodeURIComponent(document.location.href);
