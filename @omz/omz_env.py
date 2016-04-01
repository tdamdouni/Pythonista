# https://forum.omz-software.com/topic/2135/telling-if-i-m-pythonista-or-editorial-or-sublime-text-or-whatever

# coding: utf-8

try:
    import editor
    filename = editor.get_current_file()
except (ImportError, AttributeError):
    try:
        # Not Pythonista or Editorial
        import whatever_sublime_text_uses
        filename = whatever_sublime_text_uses.what_is_my_filename()
    except (ImportError, AttributeError):
        print("Could not determine currently open file!")