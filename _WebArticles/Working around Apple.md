# Working around Apple

_Captured: 2015-06-09 at 10:25 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/06/17/working-around-apple/)_

[Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4) and [Editorial](https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4) have become two of the staples in my day to day workflow. Recently there have been some ripples in Apple's perception of these two apps:

> I've just resubmitted Editorial 1.1.1. It can no longer download or open .py files from Dropbox - fingers crossed.-- Ole Zorn (@olemoritz) [June 8, 2014](https://twitter.com/olemoritz/statuses/475453986263158784)

> Just submitted Pythonista 1.5 within Apple's 48h deadline. "Open in" menu integration is gone, I hope this is enough.-- Ole Zorn (@olemoritz) [June 13, 2014](https://twitter.com/olemoritz/statuses/477265243450933248)

Apple raised concerns about the ability for both of these apps to use the "Open In" menu function to get files from other sources, like Dropbox. While this functionality has been in both apps for some time, Apple went back and said both apps break the App Store policy. To meet Apple's requests, Ole Zorn ([@olemoritz](https://twitter.com/olemoritz)), creator of Pythonista and Editorial, removed the ability to use the "Open In" menu functionality. While this change appear to have satisfied Apple, it broke quite a few work processes for people who used Dropbox as their central repository for scripts and files - including me. Thankfully the beauty of using apps that can run Python is that they have a way of working around Apple's change request. Ole has shared a Python script to use a UI file picker to bring files back into Pythonista (v1.5+) or Editorial (v1.1+) from Dropbox. The script, listed below, was shared by Ole on GitHub:
    
    
    # 
    def download_file(path, dest_filename, progress=None):
    	r = requests.get(url, stream=True, headers=headers)
    		for chunk in r.iter_content(1024*10):
    			if size > 0 and callable(progress):
    				p = float(bytes_written) / float(size)
    		label = ui.Label(frame=self.bounds)
    		label.background_color = (1, 1, 1, 0.95)
    	def will_close(self):
    	def item_selected(self, sender):
    			self.status_label.hidden = False
    			self.path = os.path.split(self.path)[0]
    	def download_file(self, path):
    		download_file(path, os.path.split(path)[1], self.download_progress)
    	def download_progress(self, p):
    	def load_folder(self):
    			items.append({'title': '..', 'image': 'ionicons-arrow-up-c-32', 'up': True})
    		def c(o1, o2):
    			if u_cmp != 0:
    			if d_cmp == 0:
    		self.name = self.path
    

[This script](https://gist.github.com/omz/fb180c58c94526e2c40b#file-dropbox-file-picker-py) can be run either directly in Pythonista or used as an [Editorial workflow](http://www.editorial-workflows.com/workflow/6366299429011456/IRERjtyaHrA) to pull files from Dropbox back to the local folder of the app. So instead of opening a file in Dropbox and pushing it over to an app, like this:

![](http://share.mygeekdaddy.me/_img_BLOGX_Working_around_Apple_2014_06_17_161508.png)

I can run the script, or workflow, and pull the file I want back into the app like this:

![](http://share.mygeekdaddy.me/_img_BLOGX_Working_around_Apple_2014_06_17_163109.png)

I think the functionality offered with the Dropbox UI Picker script is a better fit for both apps. When I need to get a file I can pull it back into Pythonista or Editorial without leaving the app I'm working in. This keeps my focus on the script or post I'm working on instead of bouncing around from Dropbox's app back to the one I'm working in. So for now I've future proofed both Pythonista and Editorial from any problems of losing the "Open In" menu functionality. Thanks Ole!
