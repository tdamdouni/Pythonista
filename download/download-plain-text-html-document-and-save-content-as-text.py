# coding: utf-8

# https://forum.omz-software.com/topic/2648/download-plain-text-html-document-and-save-content-as-text

# http://www.gamefaqs.com/ps3/959558-fallout-new-vegas/faqs/61226

# http://www.gamefaqs.com/ps3/959558-fallout-new-vegas/faqs/61226?print=1

## Download a GameFaqs.com FAQ in printable text format
## eg http://www.gamefaqs.com/ps3/959558-fallout-new-vegas/faqs/61226
## v0.1

import os, sys, re, random, appex, console, clipboard, html2text, requests, dialogs


RE_URL = re.compile(ur'^http(s)?://(www\.)?gamefaqs\.com/.*/faqs/[0-9]{3,8}$', re.IGNORECASE)


def main():
    if appex.is_running_extension():
        url = appex.get_url()
    else:
        url = clipboard.get().strip()
        if not RE_URL.match(url):
            try:
                url = console.input_alert("Enter gamefaqs URL", "", "https://www.gamefaqs.com/")
            except KeyboardInterrupt:
                sys.exit(0)
    
    newurl = "{0}?print=1".format(url)
    if RE_URL.match(url):
        h = html2text.HTML2Text()
        r = requests.get(
                         url=newurl, 
                         headers={"User-agent": "Mozilla/5.0{0:06}".format(random.randrange(999999))}
                         )
        html_content = r.text.decode('utf-8')
        rendered_content = html2text.html2text(html_content)
        filename = url.partition("gamefaqs.com/")[-1].partition("/")[-1].partition("/faqs")[0]+".txt"
        filepath = os.path.join(os.path.expanduser("~/Documents"), filename)
        
        with open(filepath, "w") as fo:
            fo.write(rendered_content)
        
        console.hud_alert("Success! Saved to '~/Documents/{0}'".format(filename), "success")
        dialogs.share_url("file:///"+filepath)

if __name__ == '__main__':
    main()
