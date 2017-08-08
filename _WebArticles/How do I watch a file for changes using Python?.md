# How do I watch a file for changes using Python?

up vote 171 down vote favorite

**92**

I have a log file being written by another process which I want to watch for changes. Each time a change occurrs I'd like to read the new data in to do some processing on it.

What's the best way to do this? I was hoping there'd be some sort of hook from the PyWin32 library. I've found the `win32file.FindNextChangeNotification` function but have no idea how to ask it to watch a specific file.

If anyone's done anything like this I'd be really grateful to hear how...

**[Edit]** I should have mentioned that I was after a solution that doesn't require polling.

**[Edit]** Curses! It seems this doesn't work over a mapped network drive. I'm guessing windows doesn't 'hear' any updates to the file the way it does on a local disk.

[python](/questions/tagged/python) [file](/questions/tagged/file) [pywin32](/questions/tagged/pywin32) [watch](/questions/tagged/watch)

[share](/q/182197)|[improve this question](/posts/182197/edit)

[edited Mar 14 '13 at 9:48](/posts/182197/revisions)

![](https://www.gravatar.com/avatar/57b2d849509d2058cee4344af8785de9?s=32&d=identicon&r=PG)

[Mariusz Jamro](/users/342473/mariusz-jamro)

13.3k84580

asked Oct 8 '08 at 11:12

![](https://www.gravatar.com/avatar/418a18dde0d9cb4cc434bd38a329190c?s=32&d=identicon&r=PG)

[Jon Cage](/users/15369/jon-cage)

16.6k1478146

add a comment | 

##  19 Answers 19

[ active](/questions/182197/how-do-i-watch-a-file-for-changes-using-python?answertab=active#tab-top) [ oldest](/questions/182197/how-do-i-watch-a-file-for-changes-using-python?answertab=oldest#tab-top) [ votes](/questions/182197/how-do-i-watch-a-file-for-changes-using-python?answertab=votes#tab-top)

up vote 45 down vote accepted

Have you already looked at the documentation available on <http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html>? If you only need it to work under Windows the 2nd example seems to be exactly what you want (if you exchange the path of the directory with the one of the file you want to watch). 

Otherwise, polling will probably be the only really platform-independent option.

**Note:** I haven't tried any of these solutions.

[share](/a/182247)|[improve this answer](/posts/182247/edit)

[edited Oct 8 '08 at 11:43](/posts/182247/revisions)

answered Oct 8 '08 at 11:29

![](https://www.gravatar.com/avatar/0ff75a365e9f11c4fe02c3d670a52e3a?s=32&d=identicon&r=PG)

[Horst Gutmann](/users/22312/horst-gutmann)

4,80311625

1

 

This answer is Windows-specific, but it appears that some cross-platform solutions to this problem have been posted here as well. - [Anderson Green](/users/975097/anderson-green) Aug 13 '13 at 22:53

  
 

Is there a benchmark, if this process is slower then implementing it in a native language like c++ ? - [user1767754](/users/1767754/user1767754) Nov 3 '14 at 14:13

add a comment | 

up vote 141 down vote

Did you try using Watchdog? <http://packages.python.org/watchdog/>

[share](/a/4690739)|[improve this answer](/posts/4690739/edit)

answered Jan 14 '11 at 11:52

![](https://www.gravatar.com/avatar/5a32c1cfc71ebf97967c5d6fd2cf2cf2?s=32&d=identicon&r=PG)

[simao](/users/87191/simao)

4,43553241

21

 

Installable with `easy_install`? Check. Free license? [Check](https://github.com/gorakhargosh/watchdog/blob/master/LICENSE). Solves the problem on the big platforms? [Check](http://packages.python.org/watchdog/installation.html#supported-platforms-and-caveats). I endorse this answer. Only note: the [example on their project page](http://packages.python.org/watchdog/quickstart.html#a-simple-example) doesn't work out of the box. Use [the one on their github](https://github.com/gorakhargosh/watchdog#example-api-usage) instead. - [Inaimathi](/users/190887/inaimathi) Oct 22 '12 at 20:25

3

 

We use watchdog. We may switch to QFileSystemWatcher. Just a fair warning- watchdog is good but far from perfect on all platforms (at this time). Each OS has it's idiosyncrasies. So, unless you are dedicated to making it perfect you will be pulling your hair out. If you are just looking to watch 10 files or so, I'd poll. OS disk caching is very mature and Watchdog involves polling APIs anyhow. It's mainly for watching huge folder structures IMHO. - [SilentSteel](/users/1086584/silentsteel) Oct 15 '13 at 23:29

1

 

My one gripe with watchdog is, that it has many dependencies. Fewer than PyQt, of course, but it doesn't work and feel like the minimal, best practice, does-one-job-and-does-it-right solution. - [AndreasT](/users/82673/andreast) Jan 15 '14 at 12:36

1

 

Is @denfromufa correct here? Does watchdog really lock files, so they can't be edited concurrently to watchdog watching them? I can hardly believe that, it would be completely useless. - [Michel Muller](/users/1501260/michel-m%c3%bcller) Dec 9 '15 at 23:24

1

 

@MichelMuller I just checked this example (see link below) and it works! not sure what was wrong before, but this answer does not provide any example. [stackoverflow.com/a/18599427/2230844](http://stackoverflow.com/a/18599427/2230844) - [denfromufa](/users/2230844/denfromufa) Dec 10 '15 at 0:24

 |  show **3** more comments

up vote 42 down vote

If polling is good enough for you, I'd just watch if the "modified time" file stat changes. To read it:

    
    
    os.stat(filename).st_mtime
    

(Also note that the Windows native change event solution does not work in all circumstances, e.g. on network drives.)

[share](/a/182259)|[improve this answer](/posts/182259/edit)

answered Oct 8 '08 at 11:34

![](https://www.gravatar.com/avatar/21aa98013e949850d41a1a0dd1c68c3a?s=32&d=identicon&r=PG)

[Deestan](/users/6848/deestan)

9,62332246

add a comment | 

up vote 30 down vote

If you want a multiplatform solution, then check [QFileSystemWatcher](http://doc.qt.nokia.com/latest/qfilesystemwatcher.html). Here an example code (not sanitized):

    
    
    from PyQt4 import QtCore
    
    @QtCore.pyqtSlot(str)
    def directory_changed(path):
        print('Directory Changed!!!')
    
    @QtCore.pyqtSlot(str)
    def file_changed(path):
        print('File Changed!!!')
    
    fs_watcher = QtCore.QFileSystemWatcher(['/path/to/files_1', '/path/to/files_2', '/path/to/files_3'])
    
    fs_watcher.connect(fs_watcher, QtCore.SIGNAL('directoryChanged(QString)'), directory_changed)
    fs_watcher.connect(fs_watcher, QtCore.SIGNAL('fileChanged(QString)'), file_changed)
    

[share](/a/5339877)|[improve this answer](/posts/5339877/edit)

[edited Jan 19 '14 at 19:11](/posts/5339877/revisions)

![](https://i.stack.imgur.com/eDsrN.jpg?s=32&g=1)

[mu 無](/users/1860929/mu-%e7%84%a1)

23.1k104065

answered Mar 17 '11 at 13:45

![](https://www.gravatar.com/avatar/124d21ba096c2e2a2e55b58a0979fb47?s=32&d=identicon&r=PG)

[hipersayan_x](/users/664435/hipersayan-x)

30133

4

 

I think that this is quite possibly the best answer of the bunch given that they either a) rely on Win32's FileSystemwatcher object and cannot be ported or b) poll for the file (which is bad for performance and will not scale). It's a pity Python doesn't have this facility built in as PyQt is a huge dependency if all you're using is teh QFileSystemWatcher class. - [CadentOrange](/users/463782/cadentorange) Oct 13 '11 at 10:07

  
 

I like this solution. I wanted to point out that you'll need a QApplication instance for it to work, I added "app = QtGui.QApplication(sys.argv)" right under the imports and then "app.exec_()" after the signal connections. - [spencewah](/users/49121/spencewah) May 2 '12 at 22:36

  
 

Just testing this on a Linux box, I'm seeing that the directory_changed method is being called, but not file_changed. - [Ken](/users/170431/ken) Nov 22 '12 at 19:08

  
 

@CadentOrange, if you don't like the pyQt dependency, [the `watchdog` package is the right answer](http://stackoverflow.com/a/4690739/667301) - [Mike Pennington](/users/667301/mike-pennington) Mar 27 '13 at 17:28

  
 

why not use `PySide` for that instead of `PyQt` for such a small use. - [Ciasto piekarz](/users/3311276/ciasto-piekarz) Sep 16 '15 at 15:22

add a comment | 

up vote 19 down vote

It should not work on windows (maybe with cygwin ?), but for unix user, you should use the "fcntl" system call. Here is an example in Python. It's mostly the same code if you need to write it in C (same function names)

    
    
    import time
    import fcntl
    import os
    import signal
    
    FNAME = "/HOME/TOTO/FILETOWATCH"
    
    def handler(signum, frame):
        print "File %s modified" % (FNAME,)
    
    signal.signal(signal.SIGIO, handler)
    fd = os.open(FNAME,  os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY,
                fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)
    
    while True:
        time.sleep(10000)
    

[share](/a/473471)|[improve this answer](/posts/473471/edit)

answered Jan 23 '09 at 16:08

![](https://www.gravatar.com/avatar/61b4e17387f9a143d28f5083988b2999?s=32&d=identicon&r=PG)

[Maxime](/users/58332/maxime)

9981223

3

 

Just incidentally, does not work on OS X. - [Grumdrig](/users/167531/grumdrig) Dec 2 '09 at 19:36

1

 

Works like a charm with Linux kernel 2.6.31 on an ext4 file system (on Ubuntu 10.04), though only for directories - it raises an IOError "not a directory" if I use it with a file. - [David Underhill](/users/164602/david-underhill) Apr 30 '10 at 0:44

1

 

GREAT! Same for me, works for directory only and watch files in this directory. But it won't work for modified files in subdirectories, so it looks like you need to walk throught subdirectories and watch all of them. (or is there a better way to do this?) - [lfagundes](/users/327812/lfagundes) Nov 8 '10 at 10:15

add a comment | 

up vote 18 down vote

Check out [pyinotify](https://github.com/seb-m/pyinotify).

inotify replaces dnotify (from an earlier answer) in newer linuxes and allows file-level rather than directory-level monitoring.

[share](/a/3031168)|[improve this answer](/posts/3031168/edit)

[edited Jul 10 '14 at 3:01](/posts/3031168/revisions)

![](https://www.gravatar.com/avatar/241b0c787ff19b6b326d1df52fac14ff?s=32&d=identicon&r=PG)

[niteshade](/users/652626/niteshade)

84511335

answered Jun 13 '10 at 5:12

![](https://www.gravatar.com/avatar/3a81daac49c660d2697a7c37737baeb8?s=32&d=identicon&r=PG)

[Michael Palmer](/users/365537/michael-palmer)

18112

  
 

+1: I've used inotify for other things since writing this script, but hadn't seen the python hook for it. Very handy :-) - [Jon Cage](/users/15369/jon-cage) Jun 14 '10 at 20:52

1

 

Not to put a damper on this answer, but after reading this article, I would say that it may not be as glamourous a solution as thought. [serpentine.com/blog/2008/01/04/why-you-should-not-use-pyinotify](http://www.serpentine.com/blog/2008/01/04/why-you-should-not-use-pyinotify/) - [NuclearPeon](/users/1703772/nuclearpeon) Nov 22 '14 at 4:53

add a comment | 

up vote 8 down vote

Well after a bit of hacking of Tim Golden's script, I have the following which seems to work quite well:

    
    
    import os
    
    import win32file
    import win32con
    
    path_to_watch = "." # look at the current directory
    file_to_watch = "test.txt" # look for changes to a file called test.txt
    
    def ProcessNewData( newData ):
        print "Text added: %s"%newData
    
    # Set up the bits we'll need for output
    ACTIONS = {
      1 : "Created",
      2 : "Deleted",
      3 : "Updated",
      4 : "Renamed from something",
      5 : "Renamed to something"
    }
    FILE_LIST_DIRECTORY = 0x0001
    hDir = win32file.CreateFile (
      path_to_watch,
      FILE_LIST_DIRECTORY,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
      None,
      win32con.OPEN_EXISTING,
      win32con.FILE_FLAG_BACKUP_SEMANTICS,
      None
    )
    
    # Open the file we're interested in
    a = open(file_to_watch, "r")
    
    # Throw away any exising log data
    a.read()
    
    # Wait for new data and call ProcessNewData for each new chunk that's written
    while 1:
      # Wait for a change to occur
      results = win32file.ReadDirectoryChangesW (
        hDir,
        1024,
        False,
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
        None,
        None
      )
    
      # For each change, check to see if it's updating the file we're interested in
      for action, file in results:
        full_filename = os.path.join (path_to_watch, file)
        #print file, ACTIONS.get (action, "Unknown")
        if file == file_to_watch:
            newText = a.read()
            if newText != "":
                ProcessNewData( newText )
    

It could probably do with a load more error checking, but for simply watching a log file and doing some processing on it before spitting it out to the screen, this works well.

Thanks everyone for your input - great stuff!

[share](/a/182953)|[improve this answer](/posts/182953/edit)

answered [Oct 8 '08 at 14:05](/posts/182953/revisions)

community wiki 

  

[ Jon Cage ](/posts/182953/revisions)

add a comment | 

up vote 5 down vote

Check [my answer](http://stackoverflow.com/questions/62832/reading-data-from-a-log-file-as-a-separate-application-is-writing-to-it#63446) to a [similar question](http://stackoverflow.com/questions/62832/). You could try the same loop in Python. [This page](http://code.activestate.com/recipes/157035/) suggests:

    
    
    import time
    
    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            print line, # already has newline
    

Also see the question [tail() a file with Python](http://stackoverflow.com/questions/136168/tail-a-file-with-python).

[share](/a/182242)|[improve this answer](/posts/182242/edit)

[edited Oct 8 '08 at 11:47](/posts/182242/revisions)

answered Oct 8 '08 at 11:28

![](https://www.gravatar.com/avatar/b93ef940e9862644d2c2e3526cedcff7?s=32&d=identicon&r=PG)

[Bruno De Fraine](/users/6918/bruno-de-fraine)

18k53754

  
 

You can you sys.stdout.write(line). You code doesn't work if the file is truncated. Python has builtin function file(). - [J.F. Sebastian](/users/4279/j-f-sebastian) Oct 8 '08 at 13:04

  
 

I've posted a modified version of your code. You may incorporate it in your answer if it works for you. - [J.F. Sebastian](/users/4279/j-f-sebastian) Oct 8 '08 at 13:15

add a comment | 

up vote 4 down vote

Well, since you are using Python, you can just open a file and keep reading lines from it.

    
    
    f = open('file.log')
    

If the line read is **not empty**, you process it.

    
    
    line = f.readline()
    if line:
        // Do what you want with the line
    

You may be missing that it is ok to keep calling `readline` at the EOF. It will just keep returning an empty string in this case. And when something is appended to the log file, the reading will continue from where it stopped, as you need.

If you are looking for a solution that uses events, or a particular library, please specify this in your question. Otherwise, I think this solution is just fine.

[share](/a/182441)|[improve this answer](/posts/182441/edit)

answered Oct 8 '08 at 12:18

![](https://www.gravatar.com/avatar/1889a3f7d589166f693da3af2da4fad7?s=32&d=identicon&r=PG)

[seuvitor](/users/23477/seuvitor)

224128

  
 

I agree, but I was after a solution that didn't require polling - [Jon Cage](/users/15369/jon-cage) Oct 8 '08 at 14:13

add a comment | 

up vote 4 down vote

Simplest solution for me is using watchdog's tool watchmedo

From <https://pypi.python.org/pypi/watchdog> I now have a process that looks up the sql files in a directory and executes them if necessary. 

    
    
    watchmedo shell-command \
    --patterns="*.sql" \
    --recursive \
    --command='~/Desktop/load_files_into_mysql_database.sh' \
    .
    

[share](/a/24410417)|[improve this answer](/posts/24410417/edit)

answered Jun 25 '14 at 13:43

![](https://www.gravatar.com/avatar/68168f9fac1a69a5023b7390d598e447?s=32&d=identicon&r=PG)

[redestructa](/users/1926824/redestructa)

486168

add a comment | 

up vote 3 down vote

Here is a simplified version of Kender's code that appears to do the same trick and does not import the entire file:

    
    
    # Check file for new data.
    
    import time
    
    f = open(r'c:\temp\test.txt', 'r')
    
    while True:
    
        line = f.readline()
        if not line:
            time.sleep(1)
            print 'Nothing New'
        else:
            print 'Call Function: ', line
    

[share](/a/1867970)|[improve this answer](/posts/1867970/edit)

[edited Dec 8 '09 at 16:13](/posts/1867970/revisions)

![](https://www.gravatar.com/avatar/e6488132d206883770017ba97d0f521f?s=32&d=identicon&r=PG)

[SilentGhost](/users/12855/silentghost)

112k30209231

answered Dec 8 '09 at 16:09

![](https://www.gravatar.com/avatar/0ab4dbf56bc78ad005104250b3b649a9?s=32&d=identicon&r=PG)

[AlaXul](/users/227261/alaxul)

311

add a comment | 

up vote 2 down vote

As you can see in [Tim Golden's article](http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html), pointed by [Horst Gutmann](http://stackoverflow.com/users/22312/horst-gutmann), WIN32 is relatively complex and watches directories, not a single file.

I'd like to suggest you look into [IronPython](http://www.codeplex.com/IronPython), which is a _.NET_ python implementation. With IronPython you can use all the _.NET_ functionality - including

    
    
    System.IO.FileSystemWatcher
    

Which handles single files with a simple _Event_ interface.

[share](/a/182297)|[improve this answer](/posts/182297/edit)

answered Oct 8 '08 at 11:42

![](https://www.gravatar.com/avatar/fd7da9bf7b009ceb7a7037906361c9eb?s=32&d=identicon&r=PG)

[gimel](/users/6491/gimel)

38.5k84885

  
 

I'd rather not have to use .net but thanks - [Jon Cage](/users/15369/jon-cage) Oct 8 '08 at 14:11

  
 

@JonCage : why not can you share the reason please ? - [Ciasto piekarz](/users/3311276/ciasto-piekarz) Sep 16 '15 at 15:26

  
 

@Ciasto because then you have to have Iron Python available rather than a basic Python installation. - [Jon Cage](/users/15369/jon-cage) Sep 17 '15 at 13:05

add a comment | 

up vote 2 down vote

This is another modification of Tim Goldan's script that runs on linux and adds a simple watcher for file modification by using a dict (file=>time).

usage: whateverName.py path_to_dir_to_watch

    
    
    #!/usr/bin/env python
    
    import os, sys, time
    
    def files_to_timestamp(path):
        files = [os.path.join(path, f) for f in os.listdir(path)]
        return dict ([(f, os.path.getmtime(f)) for f in files])
    
    if __name__ == "__main__":
    
        path_to_watch = sys.argv[1]
        print "Watching ", path_to_watch
    
        before = files_to_timestamp(path_to_watch)
    
        while 1:
            time.sleep (2)
            after = files_to_timestamp(path_to_watch)
    
            added = [f for f in after.keys() if not f in before.keys()]
            removed = [f for f in before.keys() if not f in after.keys()]
            modified = []
    
            for f in before.keys():
                if not f in removed:
                    if os.path.getmtime(f) != before.get(f):
                        modified.append(f)
    
            if added: print "Added: ", ", ".join(added)
            if removed: print "Removed: ", ", ".join(removed)
            if modified: print "Modified ", ", ".join(modified)
    
            before = after
    

[share](/a/15071134)|[improve this answer](/posts/15071134/edit)

[edited Feb 25 '13 at 17:12](/posts/15071134/revisions)

answered Feb 25 '13 at 16:05

![](https://i.stack.imgur.com/SEVHn.png?s=32&g=1)

[ronedg](/users/1453618/ronedg)

423510

add a comment | 

up vote 1 down vote

    
    
    ACTIONS = {
      1 : "Created",
      2 : "Deleted",
      3 : "Updated",
      4 : "Renamed from something",
      5 : "Renamed to something"
    }
    FILE_LIST_DIRECTORY = 0x0001
    
    class myThread (threading.Thread):
        def __init__(self, threadID, fileName, directory, origin):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.fileName = fileName
            self.daemon = True
            self.dir = directory
            self.originalFile = origin
        def run(self):
            startMonitor(self.fileName, self.dir, self.originalFile)
    
    def startMonitor(fileMonitoring,dirPath,originalFile):
        hDir = win32file.CreateFile (
            dirPath,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        # Wait for new data and call ProcessNewData for each new chunk that's
        # written
        while 1:
            # Wait for a change to occur
            results = win32file.ReadDirectoryChangesW (
                hDir,
                1024,
                False,
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                None,
                None
            )
            # For each change, check to see if it's updating the file we're
            # interested in
            for action, file_M in results:
                full_filename = os.path.join (dirPath, file_M)
                #print file, ACTIONS.get (action, "Unknown")
                if len(full_filename) == len(fileMonitoring) and action == 3:
                    #copy to main file
                    ...
    

[share](/a/18947445)|[improve this answer](/posts/18947445/edit)

[edited Jun 29 '15 at 16:26](/posts/18947445/revisions)

![](https://i.stack.imgur.com/VjcbL.jpg?s=32&g=1)

[martineau](/users/355230/martineau)

34.1k64682

answered Sep 22 '13 at 18:40

![](https://i.stack.imgur.com/KdBDY.png?s=32&g=1)

[imp](/users/2622785/imp)

196418

add a comment | 

up vote 0 down vote

You might want to take a look at this:

  * <http://code.activestate.com/recipes/577968-log-watcher-tail-f-log>

By default it "watches" a whole directory rather than a single file but the modification should be pretty straightforward.

[share](/a/8368248)|[improve this answer](/posts/8368248/edit)

answered Dec 3 '11 at 14:14

![](https://www.gravatar.com/avatar/cb39a0651b7721d2baede607f47adc9d?s=32&d=identicon&r=PG)

[Giampaolo Rodola](/users/376587/giampaolo-rodol%c3%a0)

4,58323635

1

 

This is a polling solution. He's said he's not interested in polling (and there are other _much_ simpler solutions already posted). - [Chris Morgan](/users/497043/chris-morgan) Dec 3 '11 at 14:24

add a comment | 

up vote 0 down vote

This is an example of checking a file for changes. One that may not be the best way of doing it, but it sure is a short way.

Handy tool for restarting application when changes have been made to the source. I made this when playing with pygame so I can see effects take place immediately after file save.

When used in pygame make sure the stuff in the 'while' loop is placed in your game loop aka update or whatever. Otherwise your application will get stuck in an infinite loop and you will not see your game updating.

    
    
    file_size_stored = os.stat('neuron.py').st_size
    
      while True:
        try:
          file_size_current = os.stat('neuron.py').st_size
          if file_size_stored != file_size_current:
            restart_program()
        except: 
          pass
    

In case you wanted the restart code which I found on the web. Here it is. (Not relevant to the question, though it could come in handy)

    
    
    def restart_program(): #restart application
        python = sys.executable
        os.execl(python, python, * sys.argv)
    

Have fun making electrons do what you want them to do.

[share](/a/23181354)|[improve this answer](/posts/23181354/edit)

answered Apr 20 '14 at 11:11

![](https://www.gravatar.com/avatar/7ca483cd18e813a5817aa8db515ae89a?s=32&d=identicon&r=PG)

[Bassim Huis](/users/1065762/bassim-huis)

275

  
 

Seems like using `.st_mtime` instead of `.st_size` would be more reliable and an equally short way of doing this, although the OP has indicated that he didn't want to do it via polling. - [martineau](/users/355230/martineau) Jun 29 '15 at 16:40

add a comment | 

up vote 0 down vote

If you have [Windows Server 2003 Resource Kit Tools](http://www.microsoft.com/en-us/download/details.aspx?id=17657) installed, you can start a TAIL command in a subprocess.

[share](/a/30014905)|[improve this answer](/posts/30014905/edit)

answered May 3 '15 at 14:22

![](https://lh6.googleusercontent.com/-hUdeBFUnoE0/AAAAAAAAAAI/AAAAAAAAAEI/5KnZmB8LgEY/photo.jpg?sz=32)

[L'Fish](/users/4859382/lfish)

1

add a comment | 

up vote -2 down vote

I don't know any Windows specific function. You could try getting the MD5 hash of the file every second/minute/hour (depends on how fast you need it) and compare it to the last hash. When it differs you know the file has been changed and you read out the newest lines.

[share](/a/182234)|[improve this answer](/posts/182234/edit)

[edited Oct 8 '08 at 11:45](/posts/182234/revisions)

answered Oct 8 '08 at 11:25

![](https://www.gravatar.com/avatar/ade779116850e516f0655f4dbab494e0?s=32&d=identicon&r=PG)

[daddz](/users/8942/daddz)

3,19411639

  
 

I'd rather do it without polling - [Jon Cage](/users/15369/jon-cage) Oct 8 '08 at 14:11

add a comment | 

up vote -6 down vote

I'd try something like this.

    
    
        try:
                f = open(filePath)
        except IOError:
                print "No such file: %s" % filePath
                raw_input("Press Enter to close window")
        try:
                lines = f.readlines()
                while True:
                        line = f.readline()
                        try:
                                if not line:
                                        time.sleep(1)
                                else:
                                        functionThatAnalisesTheLine(line)
                        except Exception, e:
                                # handle the exception somehow (for example, log the trace) and raise the same exception again
                                raw_input("Press Enter to close window")
                                raise e
        finally:
                f.close()
    

The loop checks if there is a new line(s) since last time file was read - if there is, it's read and passed to the `functionThatAnalisesTheLine` function. If not, script waits 1 second and retries the process. 

[share](/a/182235)|[improve this answer](/posts/182235/edit)

answered Oct 8 '08 at 11:26

![](https://www.gravatar.com/avatar/32cdc777a19a6f2b2129decd30061cd1?s=32&d=identicon&r=PG)

[kender](/users/4172/kender)

30.1k1878120

4

 

-1: Opening the file and reading lines isn't a great idea when the files could be 100's of MB big. You'd have to run it for each and every file too which would be bad when you want to watch 1000's of files. - [Jon Cage](/users/15369/jon-cage) Aug 4 '09 at 8:48

  
 

Really? Opening the file for changes? - [Farsheed](/users/895659/farsheed) Sep 15 '14 at 21:05

add a comment | 


