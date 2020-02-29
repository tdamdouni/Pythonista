from __future__ import print_function
print("""
     _______________                                                     
    |,----------.  |\   
    ||           |=| |        YouTube                                           
    ||          || | |         Video
    ||       . _o| | | __    Downloader
    |`-----------' |/ /~/
     ~~~~~~~~~~~~~~~ / /
                     ~~                                                                                                                                                                                                                                                                                                           
""")

import urllib2, urlparse, sys, webbrowser
import platform


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

#Fragt ab, ob es sich um ein iPhone oder iPad handelt
version = platform.machine()

if version == 'iPad2,5':
 order_preference = ['22', '18', '34', '35']
else: 
	order_preference = ['18', '22', '34', '35']



 
def main():
    v_id = None
    if (len(sys.argv) > 0):
        try:
            v_id = urlparse.parse_qs(sys.argv[1].split('?')[1])['v'][0]
        except Exception:
            v_id = None
    if not v_id:
        print(repr(sys.argv))
        return
    config = urllib2.urlopen('http://www.youtube.com/get_video_info?&video_id=%s&el=detailpage&ps=default&eurl=&gl=US&hl=en' % v_id).read()
    config = urlparse.parse_qs(config)
    formats = [urlparse.parse_qs(x) for x in config['url_encoded_fmt_stream_map'][0].split(',')]
    filtered_formats = dict([(x.get('itag', [0])[0], x) for x in formats if x.get('itag', [0])[0] in order_preference])
    sorted_formats   = [filtered_formats[x] for x in order_preference if filtered_formats.has_key(x)]
    first_pick = sorted_formats[0]
    download_url = first_pick['url'][0]
    if first_pick.has_key('sig'):
        download_url += ('&signature=' + first_pick['sig'][0])
    download_url = download_url.replace('http://', 'ghttp://')
    webbrowser.open(download_url)
 
if __name__ == '__main__':
    main()
 
# Bookmarklet:
# javascript:window.location='pythonista://YoutubeDL?action=run&argv='+encodeURIComponent(document.location.href);
