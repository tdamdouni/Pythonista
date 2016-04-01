# Shellista

## An iOS Shell Written for Pythonista

On 24 Nov 2012, user "pudquick" [released the initial version of Shellista][1] on the Pythonista forums, to help Pythonista users get around the fact that there is no shell available on iOS devices.  Since the original post, many in the Pythonista community have contributed to improve the functionality of Shellista.  From pudquick's initial post:

Commands and features:

* `cd` - change directory
* `pwd` - print current working directory
* `ls` - list directory contents (and file sizes)
* `cat` - print the contents of a file
* `q/quit/exit/logoff/logout` - exit the shell
* `mkdir` - make a directory
* `mv` - move or rename files / directories
* `cp` - copy files / directories (recursively)
* `rm` - delete files / directories (recursively)
* `unzip` - unzip zip archives
* `untar` - untar tar archives
* `ungzip / gunzip` - ungzip gzipped files
* Supports `*` wildcard matches (matching any number of characters)
* Supports `?` question mark matches (matching exactly one of any character)
* Supports `[]` ranges (like `[a-z]`, `[0-9]`, `[a-f0-9]`, etc.)
* Supports `~` tilde replacement (defaults to Documents folder)
* Supports environment variables (`$HOME`, but you can expand it)
* Supports single quote escaping (special characters are disabled)
* Supports backslash escaping (for individual special characters)
* Supports double quotes (for preserving spaces, but allowing special sequences

Examples of advanced usage:
* `ls *.py */*.py` (lists all .py files in current directory and at the top level of any folders in current directory)
* `cp ~/*.py backup` (copies all python scripts in the root scripts directory to a folder named 'backup')
* `rm test[1-3]?.txt` (removes files test1a.txt, test2a.txt, test2b.txt, test2c.txt, test3-.txt, etc.)

This is an intial (rough) port of a script I put together for another python interpreter on the app store. I'll be porting the rest of the commands soon: unzip, ungzip, untar, wget/curl (basic download functionality) Enjoy :)

For the interested programmer: This script uses a pure python re-implementation of some of the more basic globbing of "bash" which I wrote up myself. It's a little different than shlex, glob, or shlex+glob in that matching happens in a single parsing run through. It depends on glob for wildcard handling, but only after my code has already handled all character escapes and word parsing. An example where shlex/glob fails: In the current working directory are three files: `test apple`, `peach`, `test a*` (with an asterisk as part of the name) The command to parse is the string: `rm 'test a*'` peach shlex interprets it as `['rm', 'test a*', 'peach']`, which glob then interprets the file portion as a match of three files: `['test apple', 'test a*', 'peach']`. shlex unfortunately clobbers quotes that in a bash environment specify that the special character should be treated as a literal. This would result in deletion of all 3 files. With my parser, the single quotes around `'test a*'` are interpreted bash-style to mean escaping of the special character `*` - disabling it as a wildcard match and turning it into a literal match, resulting in the deletion of only two files: `test a*` and `peach`.

---

New Additions:

 - Integrate minimal pipista functionality
  - `pdown` - PyPi download
  - `psrch` - PyPi search
 - Minimal Git functionality
  - `git init` - Initialize git repo
  - `git add` - Stage one or more files
  - `git commit` - Commit staged files
  - `git clone` - clone a public repo (no auth)
  - `git push` - push commits via web
  - `git modified` - see which files are currently modified
  - `git log` - doesn't currently work
 - `untgz` - a convenience wrapper to untar and ungzip at the same time
 - Ripped @mark_tully's `wget` - thanks Mark!
 - Simple Python sub-shell by typing `shell`, `python`, or `!`
  - Running a file directly doesn't work (e.g. `python somefile.py`), though I tried
  - Single-line commands only

[1]: http://omz-forums.appspot.com/pythonista/post/5302343285342208
