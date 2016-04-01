#!/usr/bin/env python
########################################################################.......
"""filenav for Pythonista, version 2, by dgelessus.
This module contains file type and extension mappings used by other
modules.

To run filenav, use either `slim.py` (for iPhone/iPod touch/popover use)
or `full.py` (for panel view use on iPad).
"""

from __future__ import division, print_function
# Can't be bothered to properly prefix every string with an u
from __future__ import unicode_literals

import ui # Required to pre-load file icons

# Maps file extensions to short human-readable names.
FILE_EXTS = {
    "aac":           "Apple Audio",
    "aif":           "AIFF Audio",
    "aiff":          "AIFF Audio",
    "app":           "Mac or iOS App Bundle",
    "authors":       "Author List",
    "avi":           "AVI Video",
    "bin":           "Binary Data",
    "bmp":           "Microsoft Bitmap Image",
    "build":         "Build Instructions",
    "bundle":        "Bundle",
    "bz2":           "Bzip2 Archive",
    "c":             "C Source Code",
    "cache":         "Data Cache",
    "caf":           "CAF Audio",
    "cfg":           "Configuration File",
    "changelog":     "Changelog",
    "changes":       "Changelog",
    "command":       "Shell Script",
    "conf":          "Configuration File",
    "contribs":      "Contributor List",
    "contributors":  "Contributor List",
    "copyright":     "Copyright Notice",
    "copyrights":    "Copyright Notice",
    "cpgz":          "Gzip-compressed CPIO Archive",
    "cpio":          "CPIO Archive",
    "cpp":           "C++ Source Code",
    "css":           "Cascading Style Sheet",
    "csv":           "Comma-separated Values",
    "dat":           "Data",
    "db":            "Database",
    "dmg":           "Mac Disk Image",
    "doc":           "MS Word Document",
    "docx":          "MS Word Document (XML-based)",
    "dot":           "MS Word Template",
    "dotx":          "MS Word Template (XML-based)",
    "exe":           "Windows Executable",
    "fon":           "Bitmap Font",
    "gif":           "GIF Image",
    "git":           "Git Data",
    "gitignore":     "Git File Ignore List",
    "gz":            "Gzip Archive",
    "gzip":          "Gzip Archive",
    "h":             "C Header Source Code",
    "hgignore":      "Mercurial File Ignore List",
    "hgsubstate":    "Mercurial Substate",
    "hgtags":        "Mercurial Tags",
    "hpp":           "C++ Header Source Code",
    "htm":           "HTML File",
    "html":          "HTML File",
    "icns":          "Apple Icon Image",
    "in":            "Configuration File",
    "ini":           "MS INI File",
    "install":       "Install Instructions",
    "installation":  "Install Instructions",
    "itunesartwork": "iOS App Logo",
    "jpeg":          "JPEG Image",
    "jpg":           "JPEG Image",
    "js":            "JavaScript",
    "json":          "JSON File",
    "license":       "License",
    "m4a":           "MPEG-4 Audio",
    "m4r":           "MPEG-4 Ringtone",
    "m4v":           "MPEG-4 Video",
    "makefile":      "Makefile",
    "md":            "Markdown Text",
    "mov":           "Apple MOV Video",
    "mp3":           "MPEG-3 Audio",
    "mp4":           "MPEG-4 Video",
    "nib":           "Mac or iOS Interface File",
    "odf":           "ODF Document",
    "odp":           "ODF Slideshow",
    "ods":           "ODF Spreadsheet",
    "odt":           "ODF Text",
    "ogg":           "Ogg Vorbis Audio",
    "otf":           "OpenType Font",
    "pages":         "Apple Pages Document",
    "pdf":           "PDF Document",
    "php":           "PHP Script",
    "pkl":           "Python Pickle Data",
    "plist":         "Apple Property List",
    "png":           "PNG Image",
    "pps":           "MS PowerPoint Template",
    "ppsx":          "MS PowerPoint Template (XML-based)",
    "ppt":           "MS PowerPoint Slideshow",
    "pptx":          "MS PowerPoint Slideshow (XML-based)",
    "pxd":           "Cython/Pyrex Header",
    "pxi":           "Cython/Pyrex Header",
    "py":            "Python Script",
    "pyc":           "Python Bytecode",
    "pyo":           "Python Optimized Bytecode",
    "pytheme":       "Pythonista Color Theme",
    "pyui":          "Pythonista UI File",
    "pyx":           "Cython/Pyrex Script",
    "rar":           "RAR Archive",
    "readme":        "Read Me File",
    "rst":           "reStructured Text",
    "rtf":           "RTF Document",
    "sh":            "Shell Script",
    "src":           "Source Code",
    "svg":           "Scalable Vector Graphic",
    "tar":           "Tar Archive",
    "tgz":           "Tarball",
    "trash":         "Trash",
    "ttc":           "TrueType Font Collection",
    "ttf":           "TrueType Font",
    "txt":           "Plain Text",
    "version":       "Version Details",
    "wav":           "Waveform Audio",
    "xls":           "MS Excel Spreadsheet",
    "xlsx":          "MS Excel Spreadsheet (XML-based)",
    "xlt":           "MS Excel Template",
    "xltx":          "MS Excel Template (XML-based)",
    "xml":           "XML File",
    "yml":           "YML File",
    "z":             "Compressed Archive",
    "zip":           "Zip Archive",
}

# Maps major type groups to extensions.
# One extension should *never* appear in more than one group. Results are
# otherwise unpredictable due to the unordered nature of dicts.
_TYPE_GROUPS = {
    "app":       "app exe nib pytheme pyui",
    "archive":   "bundle bz2 cpio cpgz dmg gz gzip rar tar tgz z zip",
    "audio":     "aac aif aiff caf m4a m4r mp3 ogg wav",
    "code":      """
                 c command cpp css h hpp js json makefile pxd pxi py pyx
                 sh src
                 """,
    "code_tags": "htm html php plist xml",
    "data":      "bin cache dat db pkl pyc pyo",
    "font":      "fon otf ttc ttf",
    "git":       "git gitignore",
    "image":     "bmp gif icns itunesartwork jpg jpeg png svg",
    "text":      """
                 authors build cfg changelog changes clslog conf contribs
                 contributors copyright copyrights csv doc docx dot dotx
                 hgignore hgsubstate hgtags in ini install installation
                 license md odf odp ods odt pages pdf pps ppsx ppt pptx
                 readme rst rtf txt version xls xlsx xlt xltx yml
                 """,
    "trash":     "trash",
    "video":     "avi m4v mov mp4",
}
# Flip the dict and split extension strings.
TYPE_GROUPS = {}
for group, exts in _TYPE_GROUPS.iteritems():
    TYPE_GROUPS.update({ext: group for ext in exts.split()})

# Maps major type groups to names and icon paths.
GROUP_ICONS = {
    "app":       ("Application",     "../FileUI"),
    "archive":   ("Archive",         "ionicons-filing-32"),
    "audio":     ("Audio File",      "ionicons-ios7-musical-notes-32"),
    "code":      ("Source Code",     "../FilePY"),
    "code_tags": ("Source Code",     "ionicons-code-32"),
    "data":      ("Data File",       "ionicons-social-buffer-32"),
    "file":      ("File",            "ionicons-document-32"),
    "folder":    ("Folder",          "ionicons-folder-32"),
    "font":      ("Font File",       "../fonts-selected"),
    "git":       (None,              "ionicons-social-github-32"),
    "image":     ("Image File",      "ionicons-image-32"),
    "text":      ("Plain Text File", "ionicons-document-text-32"),
    "trash":     ("Trash",           "ionicons-folder-32"),
    "video":     ("Video File",      "ionicons-ios7-film-outline-32"),
}

# Trash icon only exists in 1.6
try:
    import dialogs
except ImportError:
    pass
else:
    GROUP_ICONS["trash"] = ("Trash", "../FolderTrash")

# Replace icon paths with ui.Image instances.
GROUP_ICONS = {k: (v[0], ui.Image.named(v[1]))
               for k, v in GROUP_ICONS.iteritems()}
