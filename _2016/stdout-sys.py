# https://forum.omz-software.com/topic/232/some-thoughts-on-the-console-module/4

# http://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python  # Will only work in single threaded apps!

from contextlib import contextmanager
from StringIO import StringIO

@contextmanager
def stdoutRedirected():
    """Save current stdout, redirect stdout to an in-memory
    file and then restore stdout when leaving the 'with'
    clause."""
    saveStdout = sys.stdout  # Save the current stdout.
    sys.stdout = StringIO() # Redirect stdout > in-memory file
    try:     yield None
    finally: sys.stdout = saveStdout # Restore original stdout

redirectedText = ''  # Holds the text after 'with' completes.
with stdoutRedirected():  # Redirect stdout to in-memory file.
    print('\n'.join('This text will not appear on the console but will instead be stored in an in-memory file.'.split()))
    # Final line of 'with' clause MUST save redirected text.
    redirectedText = sys.stdout.getvalue()  # Save hidden text

print('The "with stdoutRedirected():" clause has completed.')
print('=' * 54)
print(redirectedText) # Show that we still have hidden text
