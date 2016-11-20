# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/029e2bd955ea87425d89

import pyimgur,photos,clipboard,os,console
i=photos.pick_image()
format = 'gif' if (i.format == 'GIF') else 'jpg'
i.save('img.'+format)
clipboard.set('![]('+(pyimgur.Imgur("303d632d723a549").upload_image('img.'+format, title="Uploaded-Image").link)+')')
console.hud_alert("link copied!")
os.remove('img.'+format)

