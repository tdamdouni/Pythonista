# https://forum.omz-software.com/topic/3498/error-when-trying-to-get-a-photo-attachment-in-a-mail/8

#img = appex.get_image()
f = appex.get_attachments()
img = Image.open(f[0])
