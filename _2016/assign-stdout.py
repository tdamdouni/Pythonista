# https://forum.omz-software.com/topic/499/how-to-reset-stdout-to-the-normal-stdout-after-temporarily-reassigning-it/2

default_stdout = sys.stdout
file_handle = open('output_file', 'w')
try:
    sys.stdout = file_handle
    sys.stdout.write('foo bar')
finally:
    # make sure to restore stdout, even if an exception occurs.
    sys.stdout = default_stdout
