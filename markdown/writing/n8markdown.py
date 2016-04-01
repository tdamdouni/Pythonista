import markdown
import re
from sys import argv, exit
from hashlib import md5
import webbrowser
import clipboard

def fix_links(text):
    links_fixed = re.sub(r'(?<!<a target="_blank") href="(?!(http://(www\.)?n8henrie\.com|#))', ' target="_blank" href="', text)

    return links_fixed

def fix_code(text):
    fix_code_open = re.sub(r'<pre><code>',r'<pre>',text)
    fix_code_close = re.sub(r'</code></pre>',r'</pre>', fix_code_open)
    
    return fix_code_close

def main():
    post_file = clipboard.get()
	
    markdownified = markdown.markdown(post_file)

    links_fixed = fix_links(markdownified)
    
    code_fixed = fix_code(links_fixed)

    final_text = code_fixed

    clipboard.set( unicode(final_text) )
    webbrowser.open('wordpress://')

if __name__ == "__main__":
    main()

