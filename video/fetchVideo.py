#!/usr/bin/env python3

# https://github.com/abdalla-alothman/fetchVideo

# https://github.com/NFicano/pytube

import re, urllib.request, sys, os
from pytube import YouTube

def downloadURL(fileName, qurl):
	rq = urllib.request.urlopen(qurl)
	fSize = int(rq.info()['Content-Length'])
	print("File szie: {} bytes.".format(fSize))
	qf = os.path.join(os.getcwd(), fileName)
	downloadedChunk = 0
	blockSize = 2048
	
	with open(qf, "wb") as sura:
		while True:
			chunk = rq.read(blockSize)
			if not chunk:
				print("Download Complete. Stored as {}.".format(qf))
				break
			downloadedChunk += len(chunk)
			sura.write(chunk)
			progress = float(downloadedChunk) / fSize
			stat = r"Saving: {0} [{1:.2%}] of {2} bytes.".format(downloadedChunk, progress, fSize)
			stat = chr(27) + "[?25l" + stat + chr(8) * (len(stat) + 1)
			sys.stdout.write(stat)
			sys.stdout.flush()
			
if __name__ == "__main__":
	targetVid = YouTube()
	try:
		if len(sys.argv[1]) > 0 and sys.argv[1].startswith("http://www.youtube"):
			targetVid.url = sys.argv[1]
	except Exception:
		targetVid.url = input("Video URL:> ")
		
	print("Available Formats:")
	vDict = {}
	for count, x in enumerate(targetVid.videos, 1):
		v = x.video_codec
		e = x.extension
		r = x.resolution
		vDict.update({count:[v, e, r]})
		print("{}. Format: {:<20} || Extension: .{:<20} || Resolution: {:^10}".format(count, v, e, r))
		
	try:
		videoKey = input("Select the number of the video:> ")
		assert re.match(r"^[^a-zA-Z]", videoKey), "Ambiguous Entry."
		videoKey = int(videoKey)
		assert videoKey in vDict.keys(), "Invalid Number"
	except (AssertionError, ValueError):
		print("Expected a number from the provided list.")
		sys.exit()
	targetVid.filename = input("Save file as:> ")
	targetVid.filename = targetVid.filename + "." + vDict[videoKey][1]
	video = targetVid.get(vDict[videoKey][1], vDict[videoKey][2])
	downloadOK = input("Download(yes-ok/no):> ")
	if not re.match(r"(yes|ok)", downloadOK):
		sys.exit()
	else:
		try:
			downloadURL(targetVid.filename, video.url)
			sys.stdout.write(chr(27) + "[?25h")
		except KeyboardInterrupt:
			print("\nDeleteing file....")
			os.remove(targetVid.filename)
			sys.stdout.write(chr(27) + "[?25h")
			sys.exit()

