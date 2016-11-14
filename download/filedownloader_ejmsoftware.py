# https://gist.github.com/ejmsoftware/89edf288a15fde45682a

# Python file downloader for Pythonista by OMZ Software
# By: EJM Software ---- http://ejm.cloudvent.net
# Source: https://gist.github.com/89edf288a15fde45682a
# *****************************************
# This simple script uses the requests module to download files
# and the ui module to show a progress bar
# You can use this bookmarklet to download files from Safari:
# javascript:window.location='pythonista://filedownloader?action=run&argv='+encodeURIComponent(document.location.href);

import ui, console, clipboard, sys, requests, zipfile

class FileDownloader(ui.View):
    def __init__(self):
        #Setup the view
        self.name = 'File Downloader'
        self.background_color = 'white'
        #Setup the ui elements
        self.url_input = ui.TextField(frame = (0, 0, self.width, 50), flex='W', background_color='white')
        self.url_input.placeholder = 'URL'
        self.start_button = ui.Button(flex='LR', title='Download')
        self.start_button.center = (self.width * 0.5, 70)
        self.start_button.action = self.start_download
        self.loading_bar = ui.Label(frame=(0,0,0,50), flex='', background_color=(0.00, 0.50, 1.00, 0.5))
        self.activity_indicator = ui.ActivityIndicator(frame=(50,25,0,0), flex='W', alignment=ui.ALIGN_CENTER)
        #Add subviews to main view and 'present' ui
        self.add_subview(self.url_input)
        self.add_subview(self.start_button)
        self.add_subview(self.loading_bar)
        self.add_subview(self.activity_indicator)
        self.present('sheet')

    def setprogress(self, progress=0):
        self.loading_bar.width = self.width*progress/100
    
    @ui.in_background
    def start_download(self, sender):
        self.download_file(self.url_input.text)

    def download_file(self, url) :
        self.start_button.enabled = False
        self.activity_indicator.start()
        localFilename = url.split('/')[-1]
        if localFilename == '': localFilename = 'download'
        with open(localFilename, 'wb') as f:
            r = requests.get(url, stream=True)
            total_length = r.headers.get('content-length')
            if not total_length:
                f.write(r.content)
            else:
                dl = 0
                total_length = float(total_length)
                for chunk in r.iter_content(1024):
                    dl += len(chunk)
                    f.write(chunk)
                    self.setprogress(dl/total_length*100.0)
        self.start_button.enabled = True
        self.activity_indicator.stop()
        self.process_file(localFilename)
        self.close()
        
    def process_file(self, path):
        if zipfile.is_zipfile(path):
            if console.alert('Extract File?', '', 'OK'):
                zipfile.ZipFile(path).extractall()

if __name__=='__main__':
    view = FileDownloader()
    if len(sys.argv) > 1:
        view.url_input.text = sys.argv[1]
        view.download_file(sys.argv[1])
    elif '://' in clipboard.get():
        view.url_input.text = clipboard.get()
