# coding: utf-8

# https://gist.github.com/Maik-Wi/5415316

from __future__ import print_function
import requests, random, datetime, sys, webbrowser, console, urllib, clipboard, bs4

def main():
    song_page = None
    if (len(sys.argv) > 0):
        try:
            song_page = sys.argv[1]
        except Exception:
            song_page = None
    if not song_page:
        print(repr(sys.argv))
        return
    console.clear()
    
    # kopiert den Namen der Datei in die zwischenablage
    console.show_activity()
    soup = bs4.BeautifulSoup(urllib.urlopen(song_page))
    pageTitle = soup.title.string
    console.hide_activity()
    console.clear()
    clipboard.set(pageTitle)
    print(pageTitle)
    
    
    print("Grabbing:", song_page)
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'})
    print(" .. getting xtsite and js .. ")
    find_xtsite_js = sess.get(song_page).text
    xtsite = find_xtsite_js.rsplit('xtsite',1)[1].split(';',1)[0].split('"',1)[1].split('"',1)[0]
    the_js = find_xtsite_js.rsplit('m-a.sndcdn.com',1)[1].split('"',1)[0].split('/')[-1]
    print(" .. getting client_id .. ")
    new_headers = {'Accept-Encoding': 'identity', 'Connection': 'close'}
    sess.headers.update(new_headers)
    find_client_id = sess.get('http://m-a.sndcdn.com/' + the_js)
    client_id = find_client_id.content[:250].split('clientId',1)[1].split(';',1)[0].split('"',1)[1].split('"',1)[0]
    print("id:", client_id)
    today = datetime.datetime.utcnow().now()
    # ---- cookies here ----
    xtant='1'
    xtan='-'
    xtvrn='$'+xtsite+'$'
    xtidc = today.strftime('%y') + ('%02d' % (today.month-1)) + today.strftime('%d%H%M%S') + str(random.randint(10000,999999))
    sc_anonymous_id = '-'.join([str(random.randint(10000,999999)) for x in range(4)])
    # ---- end cookies ----
    sess.headers.update({'X-Requested-With': 'XMLHttpRequest'})
    new_cookies = {'xtant': xtant, 'xtan': xtan, 'xtvrn': xtvrn, 'xtidc': xtidc, 'sc_anonymous_id': sc_anonymous_id}
    print(" .. getting track id .. ")
    find_track_id = sess.get('http://m.soundcloud.com/_api/resolve?url=%s&client_id=%s&format=json' % (song_page, client_id), cookies = new_cookies, allow_redirects=False).headers['location']
    track_id = find_track_id.split('.json',1)[0].rsplit('/',1)[-1]
    print("id:", track_id)
    mp3_url = 'http://api.soundcloud.com/tracks/%s/stream?client_id=%s' % (track_id, client_id)
    download_url = mp3_url.replace('http://', 'ghttp://')
    webbrowser.open(download_url)
 
if __name__ == '__main__':
    main()
 
# Bookmarklet:
# javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://SoundcloudDL?action=run&argv='+document.location.href;%7D)();