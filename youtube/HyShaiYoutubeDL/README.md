youtube-dl - download videos from youtube.com or other video platforms

- [INSTALLATION](#installation)
- [DESCRIPTION](#description)
- [OPTIONS](#options)
- [BUGS](#bugs)
- [COPYRIGHT](#copyright)

# INSTALLATION

* Using [filedownloader.py](https://gist.github.com/elliospizzaman/89edf288a15fde45682a), download and extract the zip of this repo:
    * Set URL to `https://codeload.github.com/HyShai/youtube-dl/zip/ytdl-pythonista`.
    * Tap "Download"
    * When the Extract File alert appears, tap "OK".

Or

* Use the excellent [StaSH](https://github.com/ywangd/stash) shell and:
    
        wget https://github.com/HyShai/youtube-dl/archive/ytdl-pythonista.zip

        unzip ytdl-pythonista.zip


Be sure to move the **`youtube-dl`** folder (located in `youtube-dl-ytdl-pythonista/`) to the `site-packages` directory so it can be imported properly.

# DESCRIPTION
**youtube-dl** is a library to download videos from YouTube.com and a few more sites. 

# OPTIONS

See the complete list of available options on the main [youtube-dl page](https://github.com/rg3/youtube-dl#options). 

All of the options has not been fully tested on Pythonista, so please report any bugs that you believe are caused by Pythonista.

E.g. some of the postprocessors won't work on Pythonista (ffmpeg, avconv).


# EXAMPLES

```python
import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
```

Another simple example to watch or download (using [Documents](https://itunes.apple.com/us/app/documents-5-fast-pdf-reader/id364901807?mt=8&uo=4&at=11l6hc)):

```python
from youtube_dl_new import YoutubeDL
import webbrowser
import sys
import console

ydl = YoutubeDL({'quiet':True})

info = ydl.extract_info(sys.argv[1], download=False)

choice = console.alert('Download or Watch in Safari ','','Download','Watch')
if choice==1:
    webbrowser.open('r'+info['url'])
elif choice==2:
    webbrowser.open('safari-'+info['url'])
```

Most likely, you'll want to use various options. For a list of what can be done, have a look at [youtube_dl/YoutubeDL.py](https://github.com/HyShai/youtube-dl/blob/ytdl-pythonista/youtube_dl/YoutubeDL.py#L87). For a start, if you want to intercept youtube-dl's output, set a `logger` object.

Here's a more complete example of a program that outputs only errors (and a short message after the download is finished), and downloads/converts the video to an mp3 file:

```python
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
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
```

# BUGS

Bugs and suggestions that seem to be caused by this Pythonista port should be reported at: <https://github.com/HyShai/youtube-dl/issues> .

Other bugs and suggestions should be reported at: <https://github.com/rg3/youtube-dl/issues> . 



# COPYRIGHT

youtube-dl is released into the public domain by the copyright holders.
