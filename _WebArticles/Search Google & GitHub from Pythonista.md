# Search Google & GitHub from Pythonista

_Captured: 2015-12-17 at 14:24 from [sweetnessoffreedom.wordpress.com](https://sweetnessoffreedom.wordpress.com/projects/search-google-github-from-pythonista/)_

I'm a hack. I'll admit it. I spend more time trying to figure out why my scripts don't work than I actually do writing the code.

To that end, I got sick of going back and forth from Safari to [Pythonista](http://omz-software.com/pythonista/) and back on my iOS devices. So I created [a little script](https://gist.github.com/pfcbenjamin/c2852b22663aaa66011c) to search both Google and GitHub from within Pythonista's built-in browser. I did have StackExchange in there too, but took it out because if it has a good answer, it's usually towards the top of the Google results.

Again, the easiest way to get this into Pythonista is to copy the [link to the gist ](https://gist.github.com/pfcbenjamin/c2852b22663aaa66011c)to your clipboard and then use [Ole Zorn's `New from Gist` Script](https://gist.github.com/omz/4076735). If you're using [Workflow](https://itunes.apple.com/us/app/workflow-powerful-automation/id915249334?mt=8&uo=4&at=11l8rP), maybe the easiest way is to install [my `New from Gist` workflow](https://sweetnessoffreedom.wordpress.com/2014/12/13/workflow-to-pythonista-new-from-gist/) and run it the workflow from Safari.
    
    
    #coding: utf-8  
    '''  
    A little script to search Google or GitHub right from inside Pythonista.  
    I added the script to the action menu so I can do a quick search without leaving Pythonista.  
    I find this especially helpful if I'm researching some error my script is throwing.  
    '''
    
    import webbrowser  
    import console  
    import urllib  
    import re
    
    def SiteSearch(term,service):  
        if service == 1:  
            tencode = urllib.quote(term)  
            url = 'https://www.google.com/search?q=' + tencode  
            return webbrowser.open(url)  
        elif service == 2:  
            tencode = re.sub('\s','+',term)  
            url = 'https://gist.github.com/search?l=python&q=' + tencode  
            return webbrowser.open(url)  
        elif service == 3:  
            tencode = re.sub('\s','+',term)  
            url = 'https://github.com/search?l=Python&q=' + tencode  
            return webbrowser.open(url)  
        else:  
            console.hud_alert('Please select a service to search.','error')
    
    term = console.input_alert('Search Term')  
    service = console.alert('where would you like to search?','','Google','GitHub (Gist)','GitHub (Repo)',)
    
    #url = 'https://www.google.com/search?q=' + tencode
    
    SiteSearch(term,service)
    
