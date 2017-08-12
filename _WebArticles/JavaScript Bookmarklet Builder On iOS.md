# JavaScript Bookmarklet Builder On iOS

_Captured: 2015-11-30 at 00:11 from [unapologetic.io](http://unapologetic.io/posts/2014/01/28/javascript-bookmarklet-builder-on-ios/)_

(▼)

Yesterday, John Gruber released an update to his [Make Bookmarklet Perl script](http://daringfireball.net/2007/03/javascript_bookmarklet_builder). The script performs the following functions, as stated on Daring Fireball:

> My solution: A "Make Bookmarklet" Perl script that I run as a BBEdit filter that (1) takes as input a file containing JavaScript source code; (2) creates a bookmarklet URL from that source code; and then (3) places the bookmarklet code in a comment at the first line of your JavaScript source, but otherwise preserves your original script.

Bookmarklets are a key ingredient to a few of my Safari workflows on iOS. Most notably, when I want to link to a post on Unapologetic. I copy the text I wish to quote on the webpage, then run a bookmarklet which launches Drafts and creates a new draft with the title of the webpage and the URL formatted as a link in Markdown, and the copied text formatted as a Markdown blockquote. I have a few other bookmarklets too which I use less often, but the one thing they all have in common is that they were exceedingly annoying to manually create on my iPad.

I hadn't known about Gruber's script until I saw its update yesterday, but when I saw it I knew immediately that it was a function I wanted to be able to have access to on my iPad, not just my Mac. So, I set to work converting Gruber's Perl script into a Python script that can be run from Pythonista on an iPad or iPhone.

My script performs basically the exact same function as Gruber's. You can send your JavaScript code to Pythonista by running a URL action in Drafts, an Editorial workflow, or by simply pasting your code into the script itself in the designated area and hitting the run button (this is the default). If you choose to run the script by the default option, I purposely left a single space on either side of the input zone, marked `[YOUR CODE HERE]`, in case the code you paste in begins or ends with a single quote, which would break the three single quote comment block method being used to set the code as a string in the Python script. Leaving a space on either side will not affect your bookmarklet, as line-leading and line-trailing whitespace is removed by the script anyway. (▼)

Using Gruber's example from DF, if you were to send the Make_Bookmarklet python script the following code:
    
    
    var str = document.title;
    alert(str);
    

It would result in this code being printed to the Pythonista prompt page:
    
    
    // javascript:var%20str%20=%20document.title;alert(str);
    var str = document.title;
    alert(str);
    

And this bookmarklet being copied onto your clipboard:
    
    
    javascript:var%20str%20=%20document.title;alert(str);
    

Since there is no main document like a BBEdit text file for the code to be placed on, I just have Pythonista print it so that you can copy and paste it anywhere you wish. The bookmarklet itself will be on your clipboard when the script completes, so you can go straight to Safari (or whatever browser you use), bookmark the first page that comes up, then change that bookmark title and paste your bookmarklet in for the URL.

My script also mimics Gruber's in that if you run it on code which already has a commented out bookmarklet on the first line (i.e., the first line contains `// javascript:` somewhere inside of it), the script will cut that line out before running, so you can keep recycling the code printed out by Pythonista until you've gotten the bookmarklet right. If you wanted to, you could set it up to open the code as a new draft in Drafts or in a file in Editorial each time instead of just printing it in Pythonista. Then you could immediately go back to editing the script without copying from the Pythonista prompt and pasting it somewhere else.

Gruber set his script up to not encode every character, making the resulting bookmarklet more readable. Mine encodes a little bit more than his, but leaves some of the most popular characters unencoded. If you want encode everything you possibly can, just remove the characters in the `safe=` parameter of the `urllib.quote` command on line 31. If you want to encode less characters, add those you don't want encoded into that same parameter.

## Source Code to Make_Bookmarklet Script for Pythonista
    
    
import sys
import re
import clipboard
import urllib

if len(sys.argv) > 1:
	source_code = sys.argv[1]
else:
	source_code = ''' [YOUR CODE HERE] '''

split_code = source_code.split('\n') # Split code at newlines

# Remove first line if it is already a bookmarklet
if '// javascript:' in split_code[0]:
    split_code.pop(0)

source_code = '\n'.join(split_code) # Rejoin lines of source code without bookmarklet line (if it was present)

# Strip line-ending and line-leading whitespace
for i in range(len(split_code)):
    split_code[i] = split_code[i].rstrip()
    split_code[i] = split_code[i].lstrip()

bookmarklet = ''.join(split_code) # Rejoin code as bookmarklet with newlines removed
bookmarklet = re.sub(re.compile("//.*?\n" ) ,"" ,bookmarklet) # Kill commented lines
bookmarklet = re.sub(re.compile('/\*.*?\*/',re.DOTALL ) ,'' ,bookmarklet) # Kill block comments
bookmarklet = re.sub('\s\s+', ' ', bookmarklet) # Space runs to single spaces, tabs to spaces

# UTF-8 encode and URL escape
bookmarklet = bookmarklet.encode('utf-8')
bookmarklet = urllib.quote(bookmarklet, safe='=;()+?!')

bookmarklet = 'javascript:' + bookmarklet # Append 'javascript:' before bookmarklet

print('// ' + bookmarklet + '\n' + source_code) # Print full source code with new bookmarklet as commented first line
clipboard.set(bookmarklet) # Put bookmarklet on clipboard
    

## Running the Script With Code Sent From Drafts

If you want to send JavaScript code from Drafts to be made into a bookmarklet in Pythonista, you'll need to import one Drafts action and make sure that your Pythonista script is named "Make_Bookmarklet". (▼) The Drafts action utilizes the `[[selection]]` variable tag. This means that if you want to write your JavaScript inside of a larger body of text, then select only what you want to be made into the bookmarklet and then run the action, only the code that was selected will be sent. If you do not make a selection before running the script (i.e., you want to send the entire contents of the draft to be converted), the `[[selection]]` tag will act identically to the `[[draft]]` tag, sending the whole draft as most other actions do. (▼)

## Running the Script With Code Sent From Editorial

To run the script from Editorial, import the workflow below. Instructions are identical to those for Drafts: the Pythonista script must be named "Make_Bookmarklet" and the code sent will either be whatever text you have selected in Editorial or the entire document if you have no selected text.

[Direct Import Link for "Make Bookmarklet" Editorial Workflow](editorial://add-workflow?workflow-data=%7B%22name%22%3A%20%22Make%20Bookmarklet%22%2C%20%22actions%22%3A%20%5B%7B%22pauseWithoutShowingParameters%22%3A%20false%2C%20%22pauseBeforeRunning%22%3A%20false%2C%20%22customTitle%22%3A%20%22%22%2C%20%22parameters%22%3A%20%7B%22emptySelectionOption%22%3A%201%2C%20%22selectEntireLines%22%3A%20false%7D%2C%20%22class%22%3A%20%22WorkflowActionGetSelectedText%22%7D%2C%20%7B%22pauseWithoutShowingParameters%22%3A%20false%2C%20%22pauseBeforeRunning%22%3A%20false%2C%20%22customTitle%22%3A%20%22%22%2C%20%22parameters%22%3A%20%7B%7D%2C%20%22class%22%3A%20%22WorkflowActionURLEscape%22%7D%2C%20%7B%22pauseWithoutShowingParameters%22%3A%20false%2C%20%22pauseBeforeRunning%22%3A%20false%2C%20%22customTitle%22%3A%20%22Run%20Drafts%20Action%22%2C%20%22parameters%22%3A%20%7B%22URL%22%3A%20%7B%22text%22%3A%20%22pythonista%3A%2F%2FMake_Bookmarklet%3Faction%3Drun%26argv%3D%3F%22%2C%20%22tokenRanges%22%3A%20%7B%22%7B46%2C%201%7D%22%3A%20%22Input%22%7D%2C%20%22type%22%3A%20%22advancedText%22%7D%2C%20%22waitUntilLoaded%22%3A%20false%2C%20%22revealBrowserAutomatically%22%3A%20true%2C%20%22openIn%22%3A%201%7D%2C%20%22class%22%3A%20%22WorkflowActionOpenURL%22%7D%5D%2C%20%22description%22%3A%20%22%22%7D)

## Feedback

If you see any errors or have suggestions for the script, please [contact me](http://unapologetic.io/contact) with them.

## UPDATE:

Tweaked script so it senses whether it is being executed with a `sys.argv` argument (i.e., from an external source like Drafts or Editorial or from holding down the run button and typing code manually in Pythonista). If it is then it will use that argument for the `source_code` parameter, otherwise is will use the code in the `[YOUR CODE HERE]` slot.
