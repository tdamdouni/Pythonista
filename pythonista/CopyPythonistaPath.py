import editor
import clipboard
import console
import urllib

# editor.reload_files()
filePath = editor.get_path()

rawName = filePath[filePath.rfind('/Documents/') + 11:-3]

pythonista_url = 'pythonista://' + urllib.quote(rawName) + '?action=run&argv='
bookmarklet = ("javascript:(function(){if(document.location.href.indexOf('http')===0)document.location.href='"
                                      + pythonista_url
                                      + '\'+document.location.href;})();')

print('Pythonista url: ')
print(pythonista_url + '\n')
print('Bookmarklet:')
print(bookmarklet)

