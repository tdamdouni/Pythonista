# -*- coding: utf-8 -*-
###############################################################################
# filenav by dgelessus
# http://github.com/dgelessus/pythonista-scripts/blob/master/filenav.py
###############################################################################
# This is a standalone script, no additional files are necessary.
# By default, the navigator starts at ~ (the app sandbox root). A different
# root folder can be passed as a runtime argument - tap and hold the play icon.
# Execution from other scripts is also supported using filenav.run(path)
###############################################################################
# A note on Shellista integration:
# Shellista is expected to be importable, i. e. located in the root folder
# of Pythonista's Script Library, site-packages, or another folder in PATH.
# The original Shellista by pudquick as well as transistor1's have been tested
# and are known to work. Other forks should also be compatible, as long as
# the main code does not differ significantly.
# To use ShellistaExt by briarfox, the module and main class name need to be
# changed from Shellista to ShellistaExt and Shell to Shellista respectively.
# The plugins folder needs to be moved into PATH along with the main script.
###############################################################################

import collections # for the namedtuple fileinfo
import console     # for Quick Look and Open In
import datetime    # to format timestamps from os.stat()
import editor      # to open files
import errno       # for OSError codes
import os.path     # to navigate the file structure
import Image       # for thumbnail creation
import pwd         # to get names for UIDs
import shutil      # to copy files
import sound       # to play audio files
import stat        # to analyze stat results
import sys         # for sys.argv
import time        # to sleep in certain situations and avoid hangs
import ui          # duh
import webbrowser  # to open HTML files
try:               # to save PIL images to string
    import cStringIO as StringIO
except ImportError:
    import StringIO

def full_path(path):
    # Return absolute path with expanded ~s, input path assumed relative to cwd
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))

def rel_to_docs(path):
    # Return path relative to script library (~/Documents)
    return os.path.relpath(full_path(path), os.path.expanduser("~/Documents"))

def rel_to_app(path):
    # Return path relative to app bundle (~/Pythonista.app)
    return os.path.relpath(full_path(path), os.path.expanduser("~/Pythonista.app"))

# get location of current script, fall back to ~ if necessary

SCRIPT_ROOT = full_path("~") if sys.argv[0] == "prompt" else os.path.dirname(sys.argv[0])

if not os.path.exists(os.path.join(SCRIPT_ROOT, "temp")):
    os.mkdir(os.path.join(SCRIPT_ROOT, "temp"))

# list of file size units
SIZE_SUFFIXES = "bytes KiB MiB GiB TiB PiB EiB ZiB YiB".split()

# dict of known file extensions
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
    "cpgz":          "CPGZ Archive",
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
    "pxd":           "Pyrex Script",
    "pxi":           "Pyrex Script",
    "py":            "Python Script",
    "pyc":           "Python Bytecode",
    "pyo":           "Python Bytecode",
    "pytheme":       "Pythonista Code Theme",
    "pyui":          "Pythonista UI File",
    "pyx":           "Pyrex Script",
    "rar":           "RAR Archive",
    "readme":        "Read Me File",
    "rst":           "reStructured Text",
    "rtf":           "RTF Document",
    "sh":            "Shell Script",
    "src":           "Source Code",
    "svg":           "Scalable Vector Graphic",
    "tar":           "Tar Archive",
    "tgz":           "Tar Ball",
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
    "zip":           "Zip Archive"
             }

# dict of known file type groups and extensions
FILE_TYPES = {
    "app":       "app exe nib pytheme pyui",
    "archive":   "bundle bz2 cpgz dmg gz gzip rar tar tgz z zip",
    "audio":     "aac aif aiff caf m4a m4r mp3 ogg wav",
    "code":      """c command cpp css h hpp js json makefile pxd pxi py pyx
                    sh src""",
    "code_tags": "htm html php plist xml",
    "data":      "bin cache dat db pkl pyc pyo",
    "font":      "fon otf ttc ttf",
    "git":       "git gitignore",
    "image":     "bmp gif icns itunesartwork jpg jpeg png svg",
    "text":      """authors build cfg changelog changes clslog conf contribs
                    contributors copyright copyrights csv doc docx dot dotx
                    hgignore hgsubstate hgtags in ini install installation
                    license md odf odp ods odt pages pdf pps ppsx ppt pptx
                    readme rst rtf txt version xls xlsx xlt xltx yml""",
    "video":     "avi m4v mov mp4"
              }
FILE_TYPES = {k:tuple(v.split()) for k,v in FILE_TYPES.iteritems()}

# dict of descriptions and icons for all file type groups
FILE_DESCS_ICONS = {
    "app":       ("Application",     "../FileUI"),
    "archive":   ("Archive",         "ionicons-filing-32"),
    "audio":     ("Audio File",      "ionicons-ios7-musical-notes-32"),
    "code":      ("Source Code",     "../FilePY"),
    "code_tags": ("Source Code",     "ionicons-code-32"),
    "data":      ("Data File",       "ionicons-social-buffer-32"),
    "file":      ("File",            "ionicons-document-32"),
    "folder":    ("Folder",          "ionicons-folder-32"),
    "font":      ("Font File",       "../fonts-selected"),
    "git":       ("None",            "ionicons-social-github-32"),
    "image":     ("Image File",      "ionicons-image-32"),
    "text":      ("Plain Text File", "ionicons-document-text-32"),
    "video":     ("Video File",      "ionicons-ios7-film-outline-32"),
                   }
FILE_DESCS_ICONS = {k:(d,ui.Image.named(i)) for k,(d,i)
                        in FILE_DESCS_ICONS.iteritems()}

fileinfo = collections.namedtuple('fileinfo',
            'file_ext recognized_ext filetype filedesc icon')

def get_filetype(file_ext):
    for filetype, exts in FILE_TYPES.iteritems():
        if file_ext in exts:
            return filetype
    return None

def get_file_info(filename):
    if not isinstance(filename, str):
        return fileinfo('', '', '', '', None)
    recognized_ext_and_type = ('', '')
    for ext in os.path.basename(filename.lower()).split("."):
        filetype = get_filetype(ext)
        if filetype:
            recognized_ext_and_type = (ext, filetype)
    recognized_ext, filetype = recognized_ext_and_type
    is_dir = os.path.isdir(filename)
    if not filetype:
        filetype = "folder" if is_dir else "file"
    desc, icon = FILE_DESCS_ICONS.get(filetype, ("", None))
    # apply special descriptions, icons only to certain folders
    if is_dir and filetype not in ("app", "bundle", "git"):
        desc, folder_icon = FILE_DESCS_ICONS["folder"]
        if filetype != "archive":
            icon = folder_icon
    return fileinfo(ext, recognized_ext, filetype, desc, icon)

def get_thumbnail(path):
    def path_to_thumbnail(path):
        thumb = Image.open(path)
        thumb.thumbnail((32, 32), Image.ANTIALIAS)
        strio = StringIO.StringIO()
        thumb.save(strio, thumb.format)
        data = strio.getvalue()
        strio.close()
        return ui.Image.from_data(data)

    try:  # attempt to generate a thumbnail
        return path_to_thumbnail(path)
    except IOError as err:
        if not err.message == "broken data stream when reading image file":
            return None
        tmp_file = os.path.join(SCRIPT_ROOT, "temp/filenav-tmp.png")
        # write image as png using ui module
        with open(tmp_file, "wb") as f:
            f.write(ui.Image.named(path).to_png())
        return path_to_thumbnail(tmp_file)

class FileItem(object):
    # object representation of a file and its properties
    def __init__(self, path):
        # init
        self.path = path
        self.refresh()

    def refresh(self):
        # refresh all properties
        self.path = full_path(self.path)
        self.fileinfo = get_file_info(self.path)
        self.icon = self.fileinfo.icon
        self.icon_cached = False
        self.rel_to_docs = rel_to_docs(self.path)
        self.location, self.name = os.path.split(self.path)
        try:
            self.stat = os.stat(self.path)
        except OSError as err:
            self.stat = err

        if os.path.isdir(self.path):
            self.basetype = 0
            try:
                self.contents = os.listdir(self.path)
            except OSError as err:
                self.contents = err
        else:
            self.basetype = 1
            self.contents = []

    def __del__(self):
        del self.path
        del self.fileinfo
        del self.icon
        del self.rel_to_docs
        del self.location
        del self.name
        del self.stat
        del self.contents

    def __repr__(self):
        # repr(self) and str(self)
        return "filenav.FileItem(" + self.path + ")"

    def __eq__(self, other):
        # self == other
        return os.path.samefile(self.path, other.path) if isinstance(other, FileItem) else False

    def __ne__(self, other):
        # self != other
        return not os.path.samefile(self.path, other.path) if isinstance(other, FileItem) else False

    def __len__(self):
        # len(self)
        return len(self.contents)

    def __getitem__(self, key):
        # self[key]
        return self.contents[key]

    def __iter__(self):
        # iter(self)
        return iter(self.contents)

    def __reversed__(self):
        # reversed(self)
        return reversed(self.contents)

    def __contains__(self, item):
        # item in self
        return item in self.contents

    def isdir(self):
        # like os.path.isdir
        return self.basetype == 0

    def isfile(self):
        # like os.path.isfile
        return self.basetype == 1

    def basename(self):
        # like os.path.basename
        return self.name

    def dirname(self):
        # like os.path.dirname
        return self.location

    def join(self, *args):
        # like os.path.join
        return os.path.join(self.path, *args)

    def listdir(self):
        # like os.listdir
        if self.isdir():
            return self.contents
        else:
            err = OSError()
            err.errno = errno.ENOTDIR
            err.strerror = os.strerror(err.errno)
            err.filename = self.path
            raise err

    def samefile(self, other):
        # like os.path.samefile
        return os.path.samefile(self.path, other)

    def split(self):
        # like os.path.split
        return (self.location, self.name)

    def as_cell(self):
        # Create a ui.TableViewCell for use with FileDataSource
        cell = ui.TableViewCell("subtitle")
        cell.text_label.text = self.name
        if not self.icon_cached and self.fileinfo.filetype == 'image':
            thumb = get_thumbnail(self.path)
            if thumb:  # just-in-time creation of thumbnails
                self.icon = thumb
                self.icon_cached = True
        cell.image_view.image = self.icon
        cell.detail_text_label.text = FILE_EXTS.get(self.fileinfo.file_ext,
                                                    self.fileinfo.filedesc)
        if not isinstance(self.stat, OSError):  # if available, add size to subtitle
            cell.detail_text_label.text += " (" + format_size(self.stat.st_size, False) + ")"
        cell.accessory_type = "detail_{}button".format("disclosure_" if self.isdir() else "")
        return cell

CWD_FILE_ITEM = FileItem(os.getcwd())

class FileDataSource(object):
    # ui.TableView data source that generates a directory listing
    def __init__(self, fi=CWD_FILE_ITEM):
        # init
        self.fi = fi
        self.refresh()
        self.lists = [self.folders, self.files]

    def refresh(self):
        # Refresh the list of files and folders
        self.folders = []
        self.files = []
        for i in range(len(self.fi.contents)):
            if not isinstance(self.fi.contents[i], FileItem):
                # if it isn't already, make entries FileItems rather than strings
                self.fi.contents[i] = FileItem(self.fi.join(self.fi.contents[i]))

            if self.fi.contents[i].isdir():
                self.folders.append(self.fi.contents[i])
            else:
                self.files.append(self.fi.contents[i])

    def tableview_number_of_sections(self, tableview):
        # Return the number of sections
        return len(self.lists)

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.lists[section])

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        return self.lists[section][row].as_cell()

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        if section == 0:
            return "Folders"
        elif section == 1:
            return "Files"
        else:
            return "errsec"

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return False

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return False

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        pass

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        pass

    @ui.in_background
    def tableview_did_select(self, tableview, section, row):
        # Called when the user selects a row
        if not tableview.editing:
            fi = self.lists[section][row]
            if section == 0:
                console.show_activity()
                nav.push_view(make_file_list(fi))
                console.hide_activity()
            elif section == 1:
                filetype = fi.fileinfo.filetype
                if fi.fileinfo.file_ext in ("htm", "html"):
                    webbrowser.open("file://" + fi.path)
                    nav.close()
                elif filetype in ("code", "code_tags", "text"):
                    open_path(fi.path)
                    nav.close()
                elif filetype == "audio":
                    spath = rel_to_app(fi.path.rsplit(".", 1)[0])
                    sound.load_effect(spath)
                    sound.play_effect(spath)
                elif filetype == "image":
                    console.show_image(fi.path)
                else:
                    console.quicklook(fi.path)
                    nav.close()

    def tableview_accessory_button_tapped(self, tableview, section, row):
        # Called when the user taps a row's accessory (i) button
        nav.push_view(make_stat_view(self.lists[section][row]))

class StatDataSource(object):
    # ui.TableView data source that shows os.stat() data on a file
    def __init__(self, fi=CWD_FILE_ITEM):
        # init
        self.fi = fi
        self.refresh()
        self.lists = [("Actions", self.actions), ("Stats", self.stats), ("Flags", self.flags)]

    def refresh(self):
        # Refresh stat data
        stres = self.fi.stat
        flint = stres.st_mode

        self.actions = []
        self.stats = (
            ("stat-size", "Size", format_size(stres.st_size), "ionicons-code-working-32"),
            ("stat-ctime", "Created", format_utc(stres.st_ctime), "ionicons-document-32"),
            ("stat-atime", "Opened", format_utc(stres.st_atime), "ionicons-folder-32"),
            ("stat-mtime", "Modified", format_utc(stres.st_mtime), "ionicons-ios7-compose-32"),
            ("stat-uid", "Owner", "{udesc} ({uid}={uname})".format(uid=stres.st_uid, uname=pwd.getpwuid(stres.st_uid)[0], udesc=pwd.getpwuid(stres.st_uid)[4]), "ionicons-ios7-person-32"),
            ("stat-gid", "Owner Group", str(stres.st_gid), "ionicons-ios7-people-32"),
            ("stat-flags", "Flags", str(bin(stres.st_mode)), "ionicons-ios7-flag-32"),
                     )
        self.flags = (
            ("flag-socket", "Is Socket", str(stat.S_ISSOCK(flint)), "ionicons-ios7-flag-32"),
            ("flag-link", "Is Symlink", str(stat.S_ISLNK(flint)), "ionicons-ios7-flag-32"),
            ("flag-reg", "Is File", str(stat.S_ISREG(flint)), "ionicons-ios7-flag-32"),
            ("flag-block", "Is Block Dev.", str(stat.S_ISBLK(flint)), "ionicons-ios7-flag-32"),
            ("flag-dir", "Is Directory", str(stat.S_ISDIR(flint)), "ionicons-ios7-flag-32"),
            ("flag-char", "Is Char Dev.", str(stat.S_ISCHR(flint)), "ionicons-ios7-flag-32"),
            ("flag-fifo", "Is FIFO", str(stat.S_ISFIFO(flint)), "ionicons-ios7-flag-32"),
            ("flag-suid", "Set UID Bit", str(check_bit(flint, stat.S_ISUID)), "ionicons-ios7-flag-32"),
            ("flag-sgid", "Set GID Bit", str(check_bit(flint, stat.S_ISGID)), "ionicons-ios7-flag-32"),
            ("flag-sticky", "Sticky Bit", str(check_bit(flint, stat.S_ISVTX)), "ionicons-ios7-flag-32"),
            ("flag-uread", "Owner Read", str(check_bit(flint, stat.S_IRUSR)), "ionicons-ios7-flag-32"),
            ("flag-uwrite", "Owner Write", str(check_bit(flint, stat.S_IWUSR)), "ionicons-ios7-flag-32"),
            ("flag-uexec", "Owner Exec", str(check_bit(flint, stat.S_IXUSR)), "ionicons-ios7-flag-32"),
            ("flag-gread", "Group Read", str(check_bit(flint, stat.S_IRGRP)), "ionicons-ios7-flag-32"),
            ("flag-gwrite", "Group Write", str(check_bit(flint, stat.S_IWGRP)), "ionicons-ios7-flag-32"),
            ("flag-gexec", "Group Exec", str(check_bit(flint, stat.S_IXGRP)), "ionicons-ios7-flag-32"),
            ("flag-oread", "Others Read", str(check_bit(flint, stat.S_IROTH)), "ionicons-ios7-flag-32"),
            ("flag-owrite", "Others Write", str(check_bit(flint, stat.S_IWOTH)), "ionicons-ios7-flag-32"),
            ("flag-oexec", "Others Exec", str(check_bit(flint, stat.S_IXOTH)), "ionicons-ios7-flag-32"),
                     )

        if self.fi.isdir():
            # actions for folders
            self.actions += [
                ("shellista-cd", "Go here", "Shellista", "ionicons-ios7-arrow-forward-32"),
                            ]
        elif self.fi.isfile():
            # actions for files
            self.actions += [
                ("ios-qlook", "Preview", "Quick Look", "ionicons-ios7-eye-32"),
                ("pysta-edit", "Open in Editor", "Pythonista", "ionicons-ios7-compose-32"),
                ("pysta-cpedit", "Copy & Open", "Pythonista", "ionicons-ios7-copy-32"),
                ("pysta-cptxt", "Copy & Open as Text", "Pythonista", "ionicons-document-text-32"),
                # haven't yet been able to integrate hexviewer
                #("hexviewer-open", "Open in Hex Viewer", "hexviewer", "ionicons-pound-32"),
                ("ios-openin", "Open In and Share", "External Apps", "ionicons-ios7-paperplane-32"),
                            ]
            if self.fi.fileinfo.file_ext in ("htm", "html"):
                self.actions[-1:-1] = [
                    ("webbrowser-open", "Open Website", "webbrowser", "ionicons-ios7-world-32")]
            elif self.fi.fileinfo.filetype == "image":
                self.actions[-1:-1] = [
                    ("console-printimg", "Show in Console", "console", "ionicons-image-32")]
            elif self.fi.fileinfo.filetype == "audio":
                self.actions[-1:-1] = [
                    ("sound-playsound", "Play Sound", "sound", "ionicons-ios7-play-32")]


    def tableview_number_of_sections(self, tableview):
        # Return the number of sections
        return len(self.lists)

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.lists[section][1])

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        if section == 0:
            cell = ui.TableViewCell("subtitle")
            cell.image_view.image = ui.Image.named(self.lists[section][1][row][3])
        else:
            cell = ui.TableViewCell("value2")
        cell.text_label.text = self.lists[section][1][row][1]
        cell.detail_text_label.text = self.lists[section][1][row][2]
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        return self.lists[section][0]

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return False

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return False

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        pass

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        pass

    @ui.in_background # necessary to avoid hangs with Shellista and console modules
    def tableview_did_select(self, tableview, section, row):
        # Called when the user selects a row
        key = self.lists[section][1][row][0]
        if key == "shellista-cd":
            # Go Here - Shellista
            nav.close()
            print("Launching Shellista...")
            try:
                from Shellista import Shell
            except ImportError as err:
                print("Failed to import Shellista: " + err.message)
                print("See note on Shellista integration at the top of filenav.py.")
                print("> logout")
                return
            shell = Shell()
            shell.prompt = '> '
            shell.onecmd("cd " + self.fi.path)
            print("> cd " + self.fi.path)
            shell.cmdloop()
        elif key == "ios-qlook":
            # Preview - Quick Look
            nav.close()
            time.sleep(1) # ui thread will hang otherwise
            console.quicklook(self.fi.path)
        elif key == "pysta-edit":
            # Open in Editor - Pythonista
            open_path(self.fi.path)
            nav.close()
        elif key == "pysta-cpedit":
            # Copy & Open - Pythonista
            destdir = full_path(os.path.join(SCRIPT_ROOT, "temp"))
            if not os.path.exists(destdir):
                os.mkdir(destdir)
            destfile = full_path(os.path.join(destdir, self.fi.basename().lstrip(".")))
            shutil.copy(self.fi.path, destfile)
            editor.reload_files()
            open_path(destfile)
            nav.close()
        elif key == "pysta-cptxt":
            # Copy & Open as Text - Pythonista
            destdir = full_path(os.path.join(SCRIPT_ROOT, "temp"))
            if not os.path.exists(destdir):
                os.mkdir(destdir)
            destfile = full_path(os.path.join(destdir, self.fi.basename().lstrip(".") + ".txt"))
            shutil.copy(self.fi.path, destfile)
            editor.reload_files()
            open_path(destfile)
            nav.close()
        elif key == "console-printimg":
            # Show in Console - console
            console.show_image(self.fi.path)
        elif key == "sound-playsound":
            # Play Sound - sound
            spath = rel_to_app(self.fi.path.rsplit(".", 1)[0])
            sound.load_effect(spath)
            sound.play_effect(spath)
        elif key == "webbrowser-open":
            # Open Website - webbrowser
            webbrowser.open("file://" + self.fi.path)
            nav.close()
        elif key == "ios-openin":
            # Open In - External Apps
            if console.open_in(self.fi.path):
                nav.close()
            else:
                console.hud_alert("Failed to Open", "error")

    def tableview_accessory_button_tapped(self, tableview, section, row):
        # Called when the user taps a row's accessory (i) button
        pass

def check_bit(num, bit):
    # Check if bit is set in num
    return (num ^ bit) < num

def format_size(size, long=True):
    if size < 1024:
        return str(int(size)) + " bytes"
    else:
        size, bsize = float(size), int(size)
        i = 0
        while size >= 1024.0 and i < len(SIZE_SUFFIXES)-1:
            size = size/1024.0
            i += 1
        if long:
            return "{size:02.2f} {suffix} ({bsize} bytes)".format(size=size, suffix=SIZE_SUFFIXES[i], bsize=bsize)
        else:
            return "{size:01.1f} {suffix}".format(size=size, suffix=SIZE_SUFFIXES[i])

def format_utc(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp)) + " UTC"

def open_path(path):
    # Open an absolute path in editor
    editor.open_file(os.path.relpath(path, os.path.expanduser("~/Documents")))

def toggle_edit_proxy(parent):
    # Returns a function that toggles edit mode for parent
    def _toggle_edit(sender):
        sender.title = "Edit" if parent.editing else "Done"
        parent.set_editing(not parent.editing)
    return _toggle_edit

def close_proxy():
    # Returns a function that closes the main view
    def _close(sender):
        nav.close()
    return _close

def make_file_list(fi=CWD_FILE_ITEM):
    # Create a ui.TableView containing a directory listing of path
    lst = ui.TableView(flex="WH")
    # allow multiple selection when editing, single selection otherwise
    lst.allows_selection = True
    lst.allows_multiple_selection = False
    lst.allows_selection_during_editing = True
    lst.allows_multiple_selection_during_editing = True
    lst.background_color = 1.0
    lst.data_source = lst.delegate = FileDataSource(fi)
    lst.name = "/" if fi.path == "/" else fi.basename()
    lst.right_button_items = ui.ButtonItem(title="Edit", action=toggle_edit_proxy(lst)),
    return lst

def make_stat_view(fi=CWD_FILE_ITEM):
    # Create a ui.TableView containing stat data on path
    lst = ui.TableView(flex="WH")
    # allow single selection only outside edit mode
    lst.allows_selection = True
    lst.allows_multiple_selection = False
    lst.allows_selection_during_editing = False
    lst.allows_multiple_selection_during_editing = False
    lst.background_color = 1.0
    lst.data_source = lst.delegate = StatDataSource(fi)
    lst.name = "/" if fi.path == "/" else fi.basename()
    return lst

def run(path="~", mode="popover"):
    # Run the main UI application
    global nav

    lst = make_file_list(CWD_FILE_ITEM if full_path(path) == "~" else FileItem(path))
    lst.left_button_items = ui.ButtonItem(image=ui.Image.named("ionicons-close-24"),
                                          action=close_proxy()),
    nav = ui.NavigationView(lst)
    nav.navigation_bar_hidden = False
    nav.flex = "WH"
    if mode == "popover":
        nav.height = 1000
    nav.present(mode, hide_title_bar=True)

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "~")
