#!/usr/bin/env python
########################################################################.......
u"""filenav for Pythonista, version 2, by dgelessus.
This module only provides classes and functions required to run the main
scripts, it has no direct functionality on its own.

To run filenav, use either `slim.py` (for iPhone/iPod touch/popover use)
or `full.py` (for panel view use on iPad).
"""

from __future__ import division, print_function

import collections # For namedtuple, used to store file metadata
import console     # For various file actions
import datetime    # For timestamp formatting
import editor      # To open files in the editor
import errno       # For OSError codes
import io          # For BytesIO
import json        # To read the favorites list
import os          # For various path operations
import PIL.Image   # For thumbnail creation
import pwd         # For user information and UID resolution
import sound       # To play sound files
import shutil      # To copy files
import stat        # To understand stat results and flags
import sys         # To access runtime args
import time        # Need to sleep a few times
import ui          # For various utility functions
import webbrowser  # To display HTML files

from filenav import filetypes # File type names and mappings
##assert reload(filetypes) # Development/testing only

def full_path(path):
    u"""Return absolute path with expanded ~s, envvars and symlinks.
    Input path is assumed to be relative to cwd.
    """
    return os.path.realpath(os.path.expandvars(os.path.expanduser(path)))

# Constants
########################################################################.......

u"""Tuple of data size suffixes, ranging from bytes to Yottabytes. These
use IEEE-style naming (e. g. KiB instead of KB) to differentiate real
sizes (multiples of 1024) from approximates ones (multiples of 1000).
"""
SIZE_SUFFIXES = u"bytes KiB MiB GiB TiB PiB EiB ZiB YiB".split()

# Delay (in seconds) to wait between conflicting animations that would
# otherwise cause Pythonista to hang. This happens for example when a view
# fades out while the quick look window appears.
ANIM_DELAY = 0.7

HOME_DIR = full_path(u"~")
DOCS_DIR = os.path.join(HOME_DIR, u"Documents")
TEMP_DIR = os.path.join(DOCS_DIR, u"temp")
APP_DIR = full_path(os.path.join(os.path.dirname(os.__file__), u".."))

if not "APPDIR" in os.environ:
    os.environ["APPDIR"] = APP_DIR

if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

# Simple Utility Functions
########################################################################.......

def has_flags(num, flags):
    u"""Check if all flags are set in num. This only checks "on" bits,
    any bits that are "off" in flags may have any state in num.
    """
    return num & flags == flags

def format_size(size, longf=True):
    u"""Return the given data size shortened to the smallest unit where
    size < 1024. If longf is true, the original size in bytes is also
    appended in parentheses.
    """
    if size < 1024:
        return u"{} bytes".format(size)
    else:
        size, bsize = float(size), int(size)
        for suffix in SIZE_SUFFIXES[1:]:
            size /= 1024.0
            if size < 1024.0:
                break
        return (
            u"{size:02.2f} {suffix} ({bsize} bytes)"
            if longf else
            u"{size:02.2f} {suffix}"
        ).format(size=size, suffix=suffix, bsize=bsize)

def format_utc(timestamp):
    u"""Convert a timestamp to a human-readable UTC date and time.
    """
    return u"{} UTC".format(datetime.datetime.fromtimestamp(timestamp))

def rel_to_docs(path):
    u"""Return path relative to script library (~/Documents).
    """
    return os.path.relpath(full_path(path), os.path.expanduser(u"~/Documents"))

def rel_to_app(path):
    u"""Return path relative to app bundle (~/Pythonista.app).
    """
    return os.path.relpath(full_path(path), os.path.expanduser(u"~/Pythonista.app"))

def open_path(path):
    u"""Open the given file in the Pythonista editor, if possible
    """
    editor.open_file(rel_to_docs(path))
    console.hide_output()

def _thumb_for_path(path):
    u"""Open the given image file using the PIL library, generate
    a 32*32px thumbnail, and return it as a ui.Image.
    """
    thumb = PIL.Image.open(path)
    thumb.thumbnail((32, 32), PIL.Image.NEAREST)
    with io.BytesIO() as buf:
        thumb.save(buf, thumb.format)
        data = buf.getvalue()
    return ui.Image.from_data(data)

def get_thumbnail(path):
    u"""More robust version of _path_to_thumbnail. When an Apple-
    style PNG file is encountered that confuses PIL, the ui module
    is used to convert it to a "normal" PNG file, which is then
    passed back into _path_to_thumbnail.
    """
    try:
        return _thumb_for_path(path)
    except IOError as err:
        if not err.message == "broken data stream when reading image file":
            return None
        tmp_file = os.path.join(TEMP_DIR, u"filenav-tmp.png")
        # Write image as png using ui module
        with open(tmp_file, "wb") as f:
            f.write(ui.Image.named(path).to_png())
        return _thumb_for_path(tmp_file)

# File Metadata Classes
########################################################################.......

# namedtuple for quick access to file metadata that is (practically) guaranteed
# to remain constant for a specific path.
FileInfo = collections.namedtuple(
    "FileInfo",
    "dir name nameparts ext group desc icon"
)

def get_fileinfo(path):
    u"""Construct a FileInfo instance for path and populate it with
    appropriate metadata.
    """
    # Initialize variables with default values
    dir, name = os.path.split(path)
    nameparts = name.lower().split(os.extsep)
    ext = None
    group = basegroup = "folder" if os.path.isdir(path) else "file"
    desc, icon = filetypes.GROUP_ICONS[group]
    
    # Find last known file extension
    for part in nameparts:
        if part in filetypes.TYPE_GROUPS:
            ext = part
    
    # Update group, desc, icon accordingly
    if ext:
        group = filetypes.TYPE_GROUPS.get(ext, group)
        desc = filetypes.FILE_EXTS.get(ext, filetypes.GROUP_ICONS[group][0])
        icon = filetypes.GROUP_ICONS[group][1]
        
        # Special case - if desc is None, use default file/folder description
        if desc is None:
            desc = filetypes.GROUP_ICONS[basegroup][0]
    
    # Folders should only get certain file types applied
    if basegroup == "folder" and ext not in ("app", "bundle", "git", "trash"):
        desc, icon = filetypes.GROUP_ICONS[basegroup]
    
    return FileInfo(dir, name, nameparts, ext, group, desc, icon)

class FileItem(object):
    u"""Class representing a path and associated properties.
    All data that should remain constant for a specific path,
    except the path itself, is stored in self.constants as an
    instance of FileInfo.
    """
    def __new__(cls, path):
        # Constructor
        assert issubclass(cls, FileItem)
        
        if isinstance(path, FileItem):
            # Allow efficient "conversion" of a FileItem to its own type
            return path
        else:
            # Create a new FileItem from path
            self = super(FileItem, cls).__new__(cls)
            self.path = full_path(path)
            self.reload()
            return self
    
    def reload(self):
        u"""Reload the FileItem's non-constant data by re-
        examining the location referenced by self.path.
        """
        assert isinstance(self.path, basestring)
        
        self.constants = get_fileinfo(self.path)
        self.icon = self.constants.icon
        self.icon_cached = False
        
        try:
            self.stat = os.stat(self.path)
        except OSError as err:
            self.stat = None

        if os.path.isdir(self.path):
            self.basetype = 0
            try:
                self.contents = os.listdir(self.path)
            except OSError as err:
                self.contents = []
        else:
            self.basetype = 1
            self.contents = None
    
    def __repr__(self):
        # repr(self) and str(self)
        return "{}.FileItem({})".format(type(self).__module__, self.path)
    
    def __eq__(self, other):
        # self == other
        return (
            os.path.samefile(self.path, other.path)
            if isinstance(other, FileItem)
            else False
        )
    
    def basename(self):
        u"""Like os.path.basename(self.path).
        """
        return self.constants.name
    
    def commonprefix(self, others):
        u"""Like os.path.commonprefix([self.path] + others).
        """
        return os.path.commonprefix([self.path] + [
            fi.path
            if isinstance(fi, FileItem)
            else fi
            for fi in others
        ])
    
    def dirname(self):
        u"""Like os.path.dirname(self.path).
        """
        return self.constants.dir
    
    def isdir(self):
        u"""Like os.path.isdir(self.path).
        """
        return self.basetype == 0
    
    def isfile(self):
        u"""Like os.path.isfile(self.path).
        """
        return self.basetype == 1
    
    def join(self, *args):
        u"""Like os.path.join(self.path, *args).
        """
        return os.path.join(self.path, *args)
    
    def listdir(self):
        u"""Like os.listdir(self.path).
        """
        if self.isdir():
            return self.contents
        else:
            err = OSError()
            err.errno = errno.ENOTDIR
            err.strerror = os.strerror(err.errno)
            err.filename = self.path
            raise err
    
    def relpath(self, start):
        u"""Like os.path.relpath(self.path, start).
        """
        return os.path.relpath(
            self.path,
            (start.path if isinstance(start, FileItem) else start),
        )
    
    def samefile(self, other):
        u"""Like os.path.samefile(self.path, other). other may be
        a FileItem instance or a string.
        """
        if isinstance(other, FileItem):
            return self == other
        else:
            return os.path.samefile(self.path, other)
    
    def split(self):
        u"""Like os.path.split(self.path).
        """
        return (self.constants.dir, self.constants.name)
    
    def as_cell(self):
        u"""Create a ui.TableViewCell for this FileItem. It will
        include the name, icon (or thumbnail if an image), type,
        size, info button, and a disclosure arrow if a directory.
        """
        cell = ui.TableViewCell("subtitle")
        cell.text_label.text = self.basename()
        
        if not self.icon_cached and self.constants.group == "image":
            thumb = get_thumbnail(self.path)
            if thumb:  # Just-in-time creation of thumbnails
                self.icon = thumb
                self.icon_cached = True
        cell.image_view.image = self.icon
        
        cell.detail_text_label.text = self.constants.desc
        if self.stat is not None: # If available, add size to subtitle
            cell.detail_text_label.text += " ({})".format(format_size(self.stat.st_size, False))
        
        cell.accessory_type = "detail_disclosure_button" if self.isdir() else "detail_button"
        
        return cell

# Data Sources
########################################################################.......

class FavoritesDataSource(object):
    u"""ui.TableView data source that displays a list of favorites read
    from a JSON file.
    """
    
    def __init__(self, app, src, tableview):
        # Init
        self.app = app
        self.src = full_path(src)
        self.tableview = tableview
        self.reload()
    
    def reload(self):
        u"""Reload the list of favorites.
        """
        with open(self.src) as f:
            self.entries = json.load(f)
    
    def tableview_number_of_sections(self, tableview):
        u"""Return the number of sections.
        """
        return 1
    
    def tableview_number_of_rows(self, tableview, section):
        u"""Return the number of rows in the given section.
        """
        return len(self.entries)
    
    def tableview_cell_for_row(self, tableview, section, row):
        u"""Create and return a cell for the given section/row.
        """
        cell = ui.TableViewCell("subtitle")
        cell.text_label.text = self.entries[row][0]
        cell.detail_text_label.text = self.entries[row][1]
        cell.image_view.image = ui.Image.named("ionicons-folder-32")
        cell.accessory_type = "detail_disclosure_button"
        return cell
    
    def tableview_title_for_header(self, tableview, section):
        u"""Return a title for the given section.
        """
        pass
    
    def tableview_can_delete(self, tableview, section, row):
        u"""Whether the user should be able to delete the given row.
        """
        return True
    
    def tableview_can_move(self, tableview, section, row):
        u"""Whether a reordering control should be shown for the given
        row (in editing mode).
        """
        return True
    
    def tableview_delete(self, tableview, section, row):
        u"""Called when the user confirms deletion of the given row.
        """
        del self.entries[row]
        tableview.delete_rows([row])
        
        with open(self.src, "w") as f:
            json.dump(self.entries, f, indent=4)
    
    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        u"""Called when the user moves a row with the reordering
        control (in editing mode).
        """
        self.entries.insert(to_row, self.entries.pop(from_row))
        
        with open(self.src, "w") as f:
            json.dump(self.entries, f, indent=4)
    
    def tableview_did_select(self, tableview, section, row):
        u"""Called when the user selects a row.
        """
        if not tableview.editing:
            console.show_activity()
            self.app.push_view(self.app.make_file_list(FileItem(self.entries[row][0])))
            console.hide_activity()
    
    def tableview_accessory_button_tapped(self, tableview, section, row):
        u"""Called when the user taps a row's accessory (i) button.
        """
        if not tableview.editing:
            self.app.push_view(self.app.make_stat_view(FileItem(self.entries[row][0])))
    
    def add_favorite(self, sender):
        root = ui.View(name=u"Add Favorite")
        root.width, root.height = 300, 140
        
        path = ui.TextField()
        path.action = path.end_editing
        path.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
        path.autocorrection_type = False
        path.clear_button_mode = "while_editing"
        path.spellchecking_type = False
        path.placeholder = "Path"
        root.add_subview(path)
        path.flex = "BW"
        path.x, path.y = 10, 10
        path.width, path.height = root.width - 20, 30
        
        desc = ui.TextField()
        desc.action = desc.end_editing
        desc.clear_button_mode = "while_editing"
        desc.placeholder = "Description"
        root.add_subview(desc)
        path.flex = "BW"
        desc.x, desc.y = 10, path.y + path.height + 10
        desc.width, desc.height = root.width - 20, 30
        
        btn = ui.Button()
        btn.title = "Done"
        root.add_subview(btn)
        btn.x, btn.y = 10, desc.y + desc.height + 10
        btn.width, btn.height = root.width - 20, 50
        
        def _action(sender):
            self.entries.append([path.text, desc.text])
            self.tableview.insert_rows([len(self.entries) - 1])
        
            with open(self.src, "w") as f:
                json.dump(self.entries, f, indent=4)
            
            root.close()
        
        btn.action = _action
        
        root.present("popover")

class FileDataSource(object):
    u"""ui.TableView data source that generates a directory listing.
    """
    
    def __init__(self, app, fi, tableview):
        # Init
        self.app = app
        self.fi = fi
        self.tableview = tableview
        self.reload()
        self.lists = [self.folders, self.files]
    
    def reload(self):
        u"""Reload the list of files and folders.
        """
        assert isinstance(self.fi, FileItem)
        
        self.folders = []
        self.files = []
        
        for i, name in enumerate(self.fi.contents):
            if not isinstance(name, FileItem):
                # If they aren't already, convert contents to FileItems
                name = self.fi.contents[i] = FileItem(self.fi.join(name))

            if name.isdir():
                self.folders.append(name)
            else:
                self.files.append(name)
    
    def tableview_number_of_sections(self, tableview):
        u"""Return the number of sections.
        """
        return len(self.lists)
    
    def tableview_number_of_rows(self, tableview, section):
        u"""Return the number of rows in the given section.
        """
        return len(self.lists[section])
    
    def tableview_cell_for_row(self, tableview, section, row):
        u"""Create and return a cell for the given section/row.
        """
        return self.lists[section][row].as_cell()
    
    def tableview_title_for_header(self, tableview, section):
        u"""Return a title for the given section.
        """
        if section == 0:
            return "Folders"
        elif section == 1:
            return "Files"
        else:
            return "Unknown Section Header"
    
    def tableview_can_delete(self, tableview, section, row):
        u"""Whether the user should be able to delete the given row.
        """
        return False
    
    def tableview_can_move(self, tableview, section, row):
        u"""Whether a reordering control should be shown for the given
        row (in editing mode).
        """
        return False
    
    def tableview_delete(self, tableview, section, row):
        u"""Called when the user confirms deletion of the given row.
        """
        pass
    
    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        u"""Called when the user moves a row with the reordering
        control (in editing mode).
        """
        pass
    
    @ui.in_background # Necessary to avoid hangs with console module
    def tableview_did_select(self, tableview, section, row):
        u"""Called when the user selects a row.
        """
        if not tableview.editing:
            fi = self.lists[section][row]
            if section == 0:
                console.show_activity()
                self.app.push_view(self.app.make_file_list(fi))
                console.hide_activity()
            elif section == 1:
                group = fi.constants.group
                if fi.constants.ext in (u"htm", u"html"):
                    webbrowser.open(u"file://" + fi.path)
                    self.app.close()
                elif group in ("code", "code_tags", "text"):
                    open_path(fi.path)
                    self.app.close()
                elif group == "audio":
                    spath = rel_to_app(fi.path.rsplit(u".", 1)[0])
                    sound.load_effect(spath)
                    sound.play_effect(spath)
                elif group == "image":
                    console.show_image(fi.path)
                else:
                    self.app.close()
                    time.sleep(ANIM_DELAY)
                    console.quicklook(fi.path)
    
    def tableview_accessory_button_tapped(self, tableview, section, row):
        u"""Called when the user taps a row's accessory (i) button.
        """
        if not tableview.editing:
            self.app.push_view(self.app.make_stat_view(self.lists[section][row]))
    
    def create_new(self, sender):
        pass

class StatDataSource(object):
    u"""ui.TableView data source that shows various file metadata and statistics.
    """
    def __init__(self, app, fi, tableview):
        # Init
        assert isinstance(fi, FileItem)
        self.app = app
        self.fi = fi
        self.tableview = tableview
        self.reload()
        self.lists = [
            ("Actions", self.actions),
            ("Stats", self.stats),
            ("Flags", self.flags)
        ]
    
    def reload(self):
        u"""Reload metadata and actions.
        """
        
        self.actions = []
        
        if self.fi.stat is not None:
            stres = self.fi.stat
            flint = stres.st_mode
            
            self.stats = [
                ("stat.size", "Size", format_size(stres.st_size), "ionicons-code-working-32"),
                ("stat.ctime", "Created", format_utc(stres.st_ctime), "ionicons-document-32"),
                ("stat.atime", "Opened", format_utc(stres.st_atime), "ionicons-folder-32"),
                ("stat.mtime", "Modified", format_utc(stres.st_mtime), "ionicons-ios7-compose-32"),
                ("stat.uid", "Owner", "{udesc} ({uid}={uname})".format(
                    uid=stres.st_uid,
                    uname=pwd.getpwuid(stres.st_uid)[0],
                    udesc=pwd.getpwuid(stres.st_uid)[4],
                ), "ionicons-ios7-person-32"),
                ("stat.gid", "Owner Group", str(stres.st_gid), "ionicons-ios7-people-32"),
                ("stat.flags", "Flags", str(bin(stres.st_mode)), "ionicons-ios7-flag-32"),
            ]            
            self.flags = [
                ("flag.socket", "Is Socket", str(stat.S_ISSOCK(flint)), "ionicons-ios7-flag-32"),
                ("flag.link", "Is Symlink", str(stat.S_ISLNK(flint)), "ionicons-ios7-flag-32"),
                ("flag.reg", "Is File", str(stat.S_ISREG(flint)), "ionicons-ios7-flag-32"),
                ("flag.block", "Is Block Dev.", str(stat.S_ISBLK(flint)), "ionicons-ios7-flag-32"),
                ("flag.dir", "Is Directory", str(stat.S_ISDIR(flint)), "ionicons-ios7-flag-32"),
                ("flag.char", "Is Char Dev.", str(stat.S_ISCHR(flint)), "ionicons-ios7-flag-32"),
                ("flag.fifo", "Is FIFO", str(stat.S_ISFIFO(flint)), "ionicons-ios7-flag-32"),
                ("flag.suid", "Set UID Bit", str(has_flags(flint, stat.S_ISUID)), "ionicons-ios7-flag-32"),
                ("flag.sgid", "Set GID Bit", str(has_flags(flint, stat.S_ISGID)), "ionicons-ios7-flag-32"),
                ("flag.sticky", "Sticky Bit", str(has_flags(flint, stat.S_ISVTX)), "ionicons-ios7-flag-32"),
                ("flag.uread", "Owner Read", str(has_flags(flint, stat.S_IRUSR)), "ionicons-ios7-flag-32"),
                ("flag.uwrite", "Owner Write", str(has_flags(flint, stat.S_IWUSR)), "ionicons-ios7-flag-32"),
                ("flag.uexec", "Owner Exec", str(has_flags(flint, stat.S_IXUSR)), "ionicons-ios7-flag-32"),
                ("flag.gread", "Group Read", str(has_flags(flint, stat.S_IRGRP)), "ionicons-ios7-flag-32"),
                ("flag.gwrite", "Group Write", str(has_flags(flint, stat.S_IWGRP)), "ionicons-ios7-flag-32"),
                ("flag.gexec", "Group Exec", str(has_flags(flint, stat.S_IXGRP)), "ionicons-ios7-flag-32"),
                ("flag.oread", "Others Read", str(has_flags(flint, stat.S_IROTH)), "ionicons-ios7-flag-32"),
                ("flag.owrite", "Others Write", str(has_flags(flint, stat.S_IWOTH)), "ionicons-ios7-flag-32"),
                ("flag.oexec", "Others Exec", str(has_flags(flint, stat.S_IXOTH)), "ionicons-ios7-flag-32"),
            ]
        else:
            self.stats = [
                ("stat.error", "Error", "Failed to stat file", "ionicons-ios7-close-32"),
            ]
            self.flags = [
                ("flag.error", "Error", "Failed to stat file", "ionicons-ios7-close-32"),
            ]
        
        if self.fi.isdir():
            # Actions for folders
            self.actions += [
                # None yet
            ]
        elif self.fi.isfile():
            # Actions for files
            self.actions += [
                ("ios.quick_look", "Preview", "Quick Look", "ionicons-ios7-eye-32"),
                ("editor.edit", "Open in Editor", "editor", "ionicons-ios7-compose-32"),
                ("editor.copy_edit", "Copy & Open", "editor", "ionicons-ios7-copy-32"),
                ("editor.copy_edit_txt", "Copy & Open as .txt", "editor", "ionicons-document-text-32"),
                ("ios.open_in", "Open In and Share", "External Apps", "ionicons-ios7-paperplane-32"),
            ]
            if self.fi.constants.ext in ("htm", "html"):
                self.actions[0:0] = [
                    ("webbrowser.open", "Open Website", "webbrowser", "ionicons-ios7-world-32"),
                ]
            elif self.fi.constants.group == "image":
                self.actions[0:0] = [
                    ("console.print_image", "Show in Console", "console", "ionicons-image-32"),
                ]
            elif self.fi.constants.group == "audio":
                self.actions[0:0] = [
                    ("sound.play_sound", "Play Sound", "sound", "ionicons-ios7-play-32"),
                ]
    
    def tableview_number_of_sections(self, tableview):
        u"""Return the number of sections.
        """
        return len(self.lists)
    
    def tableview_number_of_rows(self, tableview, section):
        u"""Return the number of rows in the given section.
        """
        return len(self.lists[section][1])
    
    def tableview_cell_for_row(self, tableview, section, row):
        u"""Create and return a cell for the given section/row.
        """
        if section == 0:
            cell = ui.TableViewCell("subtitle")
            cell.image_view.image = ui.Image.named(self.lists[section][1][row][3])
        else:
            cell = ui.TableViewCell("value2")
        cell.text_label.text = self.lists[section][1][row][1]
        cell.detail_text_label.text = self.lists[section][1][row][2]
        return cell
    
    def tableview_title_for_header(self, tableview, section):
        u"""Return a title for the given section.
        """
        return self.lists[section][0]
    
    def tableview_can_delete(self, tableview, section, row):
        u"""Whether the user should be able to delete the given row.
        """
        return False
    
    def tableview_can_move(self, tableview, section, row):
        u"""Whether a reordering control should be shown for the given
        row (in editing mode).
        """
        return False
    
    def tableview_delete(self, tableview, section, row):
        u"""Called when the user confirms deletion of the given row.
        """
        pass
    
    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        u"""Called when the user moves a row with the reordering
        control (in editing mode).
        """
        pass
    
    @ui.in_background # Necessary to avoid hangs with console module
    def tableview_did_select(self, tableview, section, row):
        u"""Called when the user selects a row.
        """
        key = self.lists[section][1][row][0]
        if key == "ios.quick_look":
            # Preview - Quick Look
            self.app.close()
            time.sleep(ANIM_DELAY)
            console.quicklook(self.fi.path)
        elif key == "editor.edit":
            # Open in Editor - editor
            open_path(self.fi.path)
            self.app.close()
        elif key == "editor.copy_edit":
            # Copy & Open - editor
            destdir = full_path(os.path.join(full_path(u"~"), u"Documents/temp"))
            if not os.path.exists(destdir):
                os.mkdir(destdir)
            destfile = full_path(os.path.join(destdir, self.fi.basename().lstrip(u".")))
            shutil.copy(self.fi.path, destfile)
            editor.reload_files()
            open_path(destfile)
            self.app.close()
        elif key == "editor.copy_edit_txt":
            # Copy & Open as Text - editor
            destdir = full_path(os.path.join(full_path(u"~"), u"Documents/temp"))
            if not os.path.exists(destdir):
                os.mkdir(destdir)
            destfile = full_path(os.path.join(destdir, self.fi.basename().lstrip(u".") + u".txt"))
            shutil.copy(self.fi.path, destfile)
            editor.reload_files()
            open_path(destfile)
            self.app.close()
        elif key == "console.print_image":
            # Show in Console - console
            console.show_image(self.fi.path)
        elif key == "sound.play_sound":
            # Play Sound - sound
            spath = rel_to_app(self.fi.path.rsplit(u".", 1)[0])
            sound.load_effect(spath)
            sound.play_effect(spath)
        elif key == "webbrowser.open":
            # Open Website - webbrowser
            webbrowser.open(u"file://" + self.fi.path)
            self.app.close()
        elif key == "ios.open_in":
            # Open In - External Apps
            if console.open_in(self.fi.path):
                self.app.close()
            else:
                console.hud_alert(u"Failed to Open", "error")
    
    def tableview_accessory_button_tapped(self, tableview, section, row):
        u"""Called when the user taps a row's accessory (i) button.
        """
        pass

# FilenavApp Object
########################################################################.......

def toggle_edit_proxy(view):
    u"""Returns a function that toggles edit mode for view.
    This will swap view.(left|right)_button_items with view.delegate's
    other_(left|right)_button_items.
    (These attributes need to be on the delegate, because ui.TableView
    does not allow setting arbitrary attributes.)
    """
    def _toggle_edit(sender):
        view.left_button_items, view.delegate.other_left_button_items \
        = view.delegate.other_left_button_items, view.left_button_items
        
        view.right_button_items, view.delegate.other_right_button_items \
        = view.delegate.other_right_button_items, view.right_button_items
        
        view.set_editing(not view.editing)
    return _toggle_edit

class FilenavApp(object):
    u"""Base implementation of the filenav app controller.
    This base class defines methods (some of which are abstract) that
    every filenav implementation should support. It also includes
    utility methods to create preconfigured views bound to an app.
    """
    
    def __init__(self):
        # Init
        self.root = None
    
    def close(self):
        u"""Close the app's root view.
        """
        self.root.close()
    
    def push_view(self, view):
        u"""Push a view onto the navigation stack.
        """
        raise NotImplementedError
    
    def pop_view(self):
        u"""Pop the top view from the navigation stack.
        """
        raise NotImplementedError
    
    def make_favs_list(self, src):
        # Create a ui.TableView containing a favorites list loaded from src
        lst = ui.TableView(flex="WH")
        # Allow single selection only when not editing
        lst.allows_selection = True
        lst.allows_multiple_selection = False
        lst.allows_selection_during_editing = False
        lst.allows_multiple_selection_during_editing = False
        lst.background_color = 1.0
        lst.data_source = lst.delegate = FavoritesDataSource(self, src, lst)
        lst.name = u"Favorites"
        lst.width = 300
        
        lst.left_button_items = ()
        lst.delegate.other_left_button_items = (
            ui.ButtonItem(
                image=ui.Image.named(u"ionicons-ios7-plus-empty-32"),
                action=lst.delegate.add_favorite
            ),
        )
        lst.right_button_items = (
            ui.ButtonItem(title=u"Edit", action=toggle_edit_proxy(lst)),
        )
        lst.delegate.other_right_button_items = (
            ui.ButtonItem(title=u"Done", action=toggle_edit_proxy(lst)),
        )
        
        return lst
    
    def make_file_list(self, fi):
        # Create a ui.TableView containing a directory listing of path
        lst = ui.TableView(flex="WH")
        # Allow single selection only when not editing
        lst.allows_selection = True
        lst.allows_multiple_selection = False
        lst.allows_selection_during_editing = False
        lst.allows_multiple_selection_during_editing = False
        lst.background_color = 1.0
        lst.data_source = lst.delegate = FileDataSource(self, fi, lst)
        lst.name = u"/" if fi.path == u"/" else fi.basename()
        lst.width = 300
        
        lst.left_button_items = ()
        lst.delegate.other_left_button_items = (
            ui.ButtonItem(
                image=ui.Image.named(u"ionicons-ios7-plus-empty-32"),
                action=lst.delegate.create_new
            ),
        )
        lst.right_button_items = (
            ui.ButtonItem(title=u"Edit", action=toggle_edit_proxy(lst)),
        )
        lst.delegate.other_right_button_items = (
            ui.ButtonItem(title=u"Done", action=toggle_edit_proxy(lst)),
        )
        
        return lst
    
    def make_stat_view(self, fi):
        # Create a ui.TableView containing stat data on path
        lst = ui.TableView(flex="WH")
        # Allow single selection only when not editing
        lst.allows_selection = True
        lst.allows_multiple_selection = False
        lst.allows_selection_during_editing = False
        lst.allows_multiple_selection_during_editing = False
        lst.background_color = 1.0
        lst.data_source = lst.delegate = StatDataSource(self, fi, lst)
        lst.name = u"/" if fi.path == u"/" else fi.basename()
        lst.width = 300
        
        return lst

