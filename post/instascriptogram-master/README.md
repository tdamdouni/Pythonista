# Instascriptogram #

## About ##
Instascriptogram is a script I wrote in combination with IFTTT to allow me to automatically post Instagram photos to a [Scriptogr.am](http://scriptogr.am/) blog.

I set up a [rule][ifttt_rule] to watch my own account as well as another for a specific tag. Those pictures would then create a text file in my Dropbox account. The script then looks for these text files, creates a Scriptogram post, and move the text file to a 'logged' folder.

## Setup ##
1. Create an app on Scriptogr.am (this assumes you already have a blog there). 
	- Click on the Developers icon in your dashboard
	- Create a new app
	- Copy the app key into the scriptogram.py script
2. Get your Scriptogr.am ID  
    - This can be found in the Settings page in your dashboard  
3. Create a rule in IFTTT
    - My example rule can be found [here][ifttt_rule]  
    - Please be sure that the content of the rule stay the same  

	{{SourceUrl}}\<br\>  
	{{Url}}\<br\>  
	{{Caption}}<br\>  
	{{CreatedAt}}
4. Update the `AUTHORS_LIST` to the names of any people who may be taking pics on Instagram. This is so that the person who took the picture signs their name at the end of each post.
5. Create a cron job for the script. I run mine once an hour on a Mac Mini server

### Optional Items ###

I like getting notifications. If you use Pushover, you can add your token and user to the script. Be sure to change the `NOTIFY_ME` to `True`.

If you want to remove the tag from the caption of the picture, add the tag to `WATCHED_TAG`



[ifttt_rule]: https://ifttt.com/recipes/115652


