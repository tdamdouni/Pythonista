from __future__ import print_function
# https://github.com/g33k44/Quran-Downloader/blob/master/quran.py

# https://g33k44.wordpress.com/2015/01/30/quran-downloader/

from mechanize import Browser
br = Browser()
a = open("log.txt" , "a")
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent',' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0'),
                 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                 ('Accept-Encoding', 'gzip,deflate,sdch'),
                 ('Accept-Language', 'en-US,en;q=0.8'),
                 ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
for i in range(1,115) :
	try :
		print("[*] Downloading Sora Number %03d"%i)
		br.retrieve("http://server7.mp3quran.net/shur/%03d.mp3"%i , "%03d.mp3"%i)
		print("[+] Done")
	except :
		print("[-] %i not downloaded"%i)
		a.write(str(i)+"\n")
a.close()

