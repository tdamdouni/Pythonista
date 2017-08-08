# Schedule Tweets With Python

_Captured: 2015-06-11 at 23:50 from [www.movingelectrons.net](http://www.movingelectrons.net/blog/2014/12/14/schedule-tweets-with-python.html)_

![Schedule Tweets with Python](http://www.movingelectrons.net/images/schedule_tweets.png)

> _Background Information_

I consider Twitter a never-ending flow of text and media. Even when using lists or filters, you can't help feeling like you are missing out on information. Ideally, you should tweet when your followers are checking their feeds, which is a very challenging task. One solution is scheduling your tweets, so that they get posted at predefined times.

There are services out there like [Hootsuite](https://hootsuite.com/) and [Buffer](https://bufferapp.com/) which help you with this task, but only the top tier paid plans offer some flexibility. Since the Twitter API is fairly open, I decided to put together a Python script to schedule tweets with the option of attaching images. I have been using it for months now, and I think I have ironed out most bugs and quirks associated to it.

## Scheduling Tweets

I wanted the system to be flexible and ubiquitous, so I'm using a simple text file to hold all the tweets that will be posted. This file is in one of my folders in Dropbox, so that I can access it from pretty much any computer or mobile device connected to Internet. Images to be tweeted are also placed inside a predefined folder in Dropbox.

Each scheduled tweet is in a separate line in the text file with the following syntax:

`a|Tweet text|image_filename.ext|YYY-MM-DD@HH:MM`

The `image_filename.ext` is optional, so it can be omitted (keeping the pipe symbols) if you don't want to include an image with your tweet. Abbreviations for days of the week can also be used, and several posting dates and times can be setup for a particular tweet by separating them with commas.

So, for instance, the following line:

`a|#Commlite Canon EF to @Sony E-Mount adapter Review > http://bit.ly/Xvc3IF cc:@SonyAlphaRumors|commlite_review.png|Fri@11:45`

Generated the following tweet:

![tweet_example](https://farm8.staticflickr.com/7506/15997749466_8988b40532_o.png)

As another example, if you wanted to tweet _movingelectrons.net rocks!_ on December 4th at 11pm and on Mondays at 8am with no image attached, you would have to include a line in the text file with the following:

`a|movingelectrons.net rocks!||2014-12-04@23:00,Mon@08:00`

The `a` at the beginning is a flag to indicate the tweet is active. So, if you wanted to stop tweeting that line but keep it in the text file as reference or to be tweeted in the future, you can just replace the `a` with a different character, like `x`.

Since this is just plain old text, you can use iOS apps like [Launch Center Pro](https://itunes.apple.com/us/app/launch-center-pro/id532016360?mt=8&uo=4&at=11lqkH) or [Drafts](https://itunes.apple.com/us/app/drafts-4-quickly-capture-notes/id905337691?mt=8&uo=4&at=11lqkH) to quickly access your tweet file or come up with automation workflows.

**The scripts integrates with [Pushover app](https://itunes.apple.com/us/app/pushover-notifications/id506088175?mt=8&uo=4&at=11lqkH)**. So, if one of the tweets fails to be posted for any reason (e.g tweet larger than 140 characters after the Twitter API links to the attached image), the script will alert to a mobile device with a short description of the error.

## What You Need

  1. An always-on computer or Network Attached Storage (NAS) device. I used to use an [Asus EeeBox](http://www.amazon.com/gp/product/B008ABL14A/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008ABL14A&linkCode=as2&tag=movinelect0e-20&linkId=QJUP2TWFNF2PJ4W7) with Ubuntu for this, but some months ago I switched to a [Synology DS214Play](http://www.amazon.com/gp/product/B00FWUQNDQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00FWUQNDQ&linkCode=as2&tag=movinelect0e-20&linkId=KGFE4Y6NDDMXG3HE), and I couldn't be more happy with it. It's an awesome little server capable of doing pretty much any task my previous Linux box used to do with almost no maintenance.
  2. You should have Python installed in your computer or NAS. You also need to install the [Twython library](https://pypi.python.org/pypi/twython), which is a Python wrapper for the Twitter API.
  3. Twitter account (with the API's key, secret and tokens provided by twitter)
  4. Pushover account.
  5. Dropbox account. If you don't have one, you can just go [here](https://db.tt/LdFyqgz2) and sign up for one (it has my referral code embedded in it). 

## The Code

**Full disclaimer:** Although I worked with several programming languages in my college days, I don't consider myself a programmer. I write scripts out of the enjoyment of creating things. All the scripts in this site work and do what they are supposed to do, they may not be written in the most elegant way. If you think you can improve them, feel free to so do, I've placed them in GitHub. You can also use part of this code as long as you link back to this site.

You can find the Python script below, or you can just download it from GitHub [here](https://gist.github.com/Moving-Electrons/0fd550758b4bcc92029f). I will go over the main sections here and will briefly explain how it works. However, if you have questions, feel free to leave a comment below or send me a message. I'll reply back as soon as I can.
    
    
    #!/usr/local/bin/python2.7
    
    import datetime
    import time
    import re
    import os
    from twython import Twython
    import sys
    import traceback
    import httplib, urllib #used in the Pushover code
    
    
    #sys.stdout = open('twitter.log', 'a') #Outputs to file instead of Standard Output.
    
    # Linux:
    #folderPath = '/home/USERNAME/Dropbox/Scripts/Twitter/'
    #folderAttach = '/home/USERNAME/Dropbox/Scripts/Twitter/attach/'
    
    # Synology:
    folderPath = '/SHARED_DRIVE/Dropbox/Scripts/Twitter/'
    folderAttach = '/SHARED_DRIVE/Dropbox/Scripts/Twitter/attach/'
    
    schFile = 'TweetSchedule.txt'
    
    #Posts only if current time is within 50 min of predefined post time in text file.
    #The script has been setup in the Synology to run every hour.
    postInterval = 3000
    
    # Twitter Credentials
    App_Key='INCLUDE_YOURS_HERE'
    App_Secret='INCLUDE_YOURS_HERE'
    Oauth_Token='INCLUDE_YOURS_HERE'
    Oauth_Token_Secret='INCLUDE_YOURS_HERE'
    
    
    def pushover(msg):
    
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.urlencode({
                "token": "'INCLUDE_YOURS_HERE'",
                "user": "'INCLUDE_YOURS_HERE'",
                "message": msg,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    
    
    def postTweets(tweetText, tweetAttach):
    
        twitter = Twython(App_Key, App_Secret, Oauth_Token, Oauth_Token_Secret)
    
        try:
    
            if tweetAttach=='':
    
                twitter.update_status(status=tweetText)
                print 'Successfully tweeted!'
    
            else:
                completeAttPath = folderAttach+tweetAttach
                attachment=open(completeAttPath, 'rb')
                twitter.update_status_with_media(media=attachment, status=tweetText)
                attachment.close()
    
                print 'Successfully tweeted!'
    
        except:
    
            er = traceback.format_exc()
            print 'Warning: tweet -> '+tweetText+'<- could not be tweeted'
            print 'Error:\n'+er
            msg = 'Tweet: '+tweetText+'\nError: '+er[-180:]
            pushover(msg)
    
        return
    
    
    def isItTime(freq): #receives string in the form XXX@XX:XX@XX:XX or XXXX-XX-XX@XX:XX@XX:XX per day
    
        now = datetime.datetime.now()
        postFlag = False
    
        days = freq.split(",")
        for day in days:
    
            rightDay = False
            times = day.split("@")
    
            # Determining if it is the correct date/week day:
            # ---
    
            #takes 1st item in the list - which is the date/week day - and determines which type of date it is:
            if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',times[0]):
                print 'Processing date in xxxx-xx-xx format'
    
                if times[0]==now.strftime("%Y-%m-%d"):
                    rightDay = True
                    print 'It\'s the right day'
    
            elif re.match('^[a-zA-Z]{3}$',times[0]):
                print 'Processing date in XXX format'
    
                if times[0]==now.strftime("%a"): #Weekday's as local's abbreviated name: Mon, Tue, etc.
                    rightDay = True
                    print 'It\'s the right day'
    
            else:
                print times[0]+' -> Wrong date format!'
    
    
            # Determining if it is the correct time:
            # ---
            if rightDay:
    
                for time in times[1:]: #doesn't iterate over the 1st element which is the day
                    if re.match('^[0-9]{1,2}:[0-9]{2}',time):
    
                        nowStr = now.strftime("%H:%M") #Converts datetime object to string (so that it can be converted to a time object below)
    
                        postTime = datetime.datetime.strptime(time,'%H:%M') #Converts the string into a time object
                        nowTime = datetime.datetime.strptime(nowStr,'%H:%M') 
                        diffTime = nowTime - postTime
                        diffTimeSeconds = diffTime.total_seconds()
    
                        if diffTimeSeconds>=0 and diffTimeSeconds<postInterval:
    
                            postFlag = True
                            print 'It\'s the right time'
    
                    else: 
                        print time+' -> Wrong time format!'
    
        return postFlag
    
    
    #Main Script
    
    schTweets = open(folderPath+schFile,'rU') #IMPORTANT: rU Opens the file with Universal Newline Support, so \n and/or \r is recognized as a new line. 
    tweetList = schTweets.readlines()
    schTweets.close()
    
    print '\n%s Running script...' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for tweet in tweetList:
        tweet = tweet.strip('\n')
    
        try:
            tStatus, tText, tAttach, tTimes = tweet.split('|')
            if tStatus=='a':
    
                print 'Checking time interval '+tTimes
                if isItTime(tTimes):
                    print 'Trying to post...'
                    postTweet(tText, tAttach)
                else:
                    print 'Not right time to tweet'
    
        except ValueError:
            print 'Incorrect line format. There might not be a | character in the line'
            pass
    

After importing all the needed libraries, two key variables are defined: `folderPath` stores the path where the Twitter text file will be stored. `folderAttach` stores the path to the folder containing the images to be posted. Note that in the script above, these paths point to subfolders inside Dropbox. That's the way we'll be interacting with Dropbox instead of using their API.

`schFile`has the name of the text file holding all the scheduled tweets. The variable `postInterval` holds the amount of seconds _back_ from the time the script is run, in which tweets will be allowed to be posted. In this case, 3000 seconds (i.e. 50 min). I could have used 59 minutes, but I didn't want to take chances of tweets not being posted because of differences in time. So, for example a tweet like the following:

`a|moving electrons rock!!||Tue@08:45`

Would really be posted at 9:00 am, which is the next time the script would run in my machine. Keep in mind that **the Synology box has been set up to run this script every hour**, I don't really need the script to run at a higher frequency. If you are using _Cron_ to run recurring scripts on a Linux machine or a Mac, you can find information on how to set it up [here](https://help.ubuntu.com/community/CronHowto).

Continuing with the script, your Twitter credentials are then defined, followed by the functions for sending a message through _Pushover_, the function for posting your tweets and the function for determining if it is time to post a particular tweet. These functions are called from a loop that goes through every tweet in the list/file. This loop is located in the the main body of the script, towards the end of it.

I hope you find the script useful. Let me know what you think in the comments below or if you would like a feature added.
