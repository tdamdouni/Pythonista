# coding: utf-8

# https://forum.omz-software.com/topic/2574/progress-tracker-on-app-badge/2

import requests,bs4,urllib2
import ProgressBadge as pb

#Gets the raw video url for the video using the keepvid service. 
vidurl='https://www.youtube.com/watch?v=fzievdlaVIU'
url='http://www.keepvid.com/?url={}'.format(vidurl)
soup = bs4.BeautifulSoup(urllib2.urlopen(url).read())
link=[l.get('href') for l in soup.select('a') if l.get('href') and 'googlevideo.com' in l.get('href')][0]

#Holds the progress bar
c=pb.Container()
try:
    with open('vid.mp4', "wb") as f:
        response = requests.get(link, stream=True)
        #Total length of the video
        total_length = response.headers.get('content-length')
        #The length of the video is the "top value" for our task
        task=pb.Progress(int(total_length))
        #Add this task to the container. 
        c.add(task)
        #Update the task as we download and write the video
        for data in response.iter_content():
            f.write(data)
            task.increment(len(data))
            c.update()
except:
    #Clean up, which means take away the badge from the app. 
    task.finish()
    raise
#clean up
task.finish()
