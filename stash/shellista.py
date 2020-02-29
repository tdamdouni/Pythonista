from __future__ import print_function
# https://gist.github.com/pudquick/4139094

import os, cmd, sys, re, glob, os.path, shutil, zipfile, tarfile, gzip

# Credits
#
# The python code here was written by pudquick@github 
#
# License
#
# This code is released under a standard MIT license.
#
#	Permission is hereby granted, free of charge, to any person
#	obtaining a copy of this software and associated documentation files
#	(the "Software"), to deal in the Software without restriction,
#	including without limitation the rights to use, copy, modify, merge,
#	publish, distribute, sublicense, and/or sell copies of the Software,
#	and to permit persons to whom the Software is furnished to do so,
#	subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be
#	included in all copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
#	BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
#	ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#	CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.

# You can skip over reading this class, if you like.
# It's an implementation of mine of the bash parser in pure python
# This has advantages over shlex, glob, and shlex->glob in that it expects
# the strings to represent files from the start.

class BetterParser:
    def __init__(self):
        self.env_vars = {"$HOME": os.path.expanduser('~')}
    def parse(self, instr):
        instr = instr.rstrip('\r\n\t ')
        # Handle all three steps of parsing:
        # 1: Quoting
        # 2: Expansion (vars, ~, and glob.glob)
        # 3: Splitting
        if (not instr):
            return []
        parse_array = [[],[]]
        parse_state = 0
        # Stage 1: Process quotes
        last_block = []
        for i,c in enumerate(instr):
            if (parse_state == 0):
                # Base state, look for quotes that haven't been escaped
                if (c == '\\'):
                    # Switch to special mode to escape the next character
                    last_block.append(i)
                    parse_state += 3
                elif (c == '"'):
                    # Start double quoting
                    last_block.append(i)
                    parse_state = 1
                elif (c == "'"):
                    # Start single quoting
                    last_block.append(i)
                    parse_state = 2
                else:
                    parse_array[0].append(c)
                    parse_array[1].append(0)
            elif (parse_state == 1):
                if (c not in '$\\"'):
                    parse_array[0].append(c)
                    parse_array[1].append(1)
                elif (c == '$'):
                    parse_array[0].append(c)
                    parse_array[1].append(0)
                elif (c == '\\'):
                    last_block.append(i)
                    parse_state += 3
                else:
                    last_block.pop()
                    parse_state = 0
            elif (parse_state == 2):
                if (c != "'"):
                    parse_array[0].append(c)
                    parse_array[1].append(1)
                else:
                    last_block.pop()
                    parse_state = 0
            elif (3 <= parse_state <= 4):
                last_block.pop()
                parse_array[0].append(c)
                parse_array[1].append(parse_state + 0)
                parse_state -= 3
        if (1 <= parse_state <= 2):
            raise SyntaxError("Unbalanced quotes at char %s: %s <--" % (last_block[-1],instr[:(last_block[-1]+1)]))
        elif (parse_state == 3):
            raise SyntaxError("Unfinished backslash escape at char %s: %s <--" % (last_block[-1],instr[:(last_block[-1]+1)]))
        elif (parse_state == 4):
            raise SyntaxError("Unfinished backslash escape within double quotes at char %s: %s <--" % (last_block[-1],instr[:(last_block[-1]+1)]))
        # State 1.5: Rebuild the parse array, evaluating escaped characters
        temp_array = [[],[]]
        escapes = {'t': '\t', 'r': '\r', 'n': '\n'}
        for i,c in enumerate(parse_array[0]):
            if (3 <= parse_array[1][i] <= 4):
                temp_array[0].append(escapes.get(c,c))
                temp_array[1].append(1)
            else:
                temp_array[0].append(c)
                temp_array[1].append(parse_array[1][i] + 0)
        parse_array = temp_array
        # Stage 2: Perform expansions
        for i,c in enumerate(parse_array[0]):
            if ((c == '$') and (parse_array[1][i] == 0)):
                # Unquoted $ detected
                remainder = ''.join(parse_array[0][i:])
                for var_name in self.env_vars.keys():
                    if remainder.startswith(var_name):
                        # Found a variable that needs to be replaced
                        # Blow out the variable name
                        for j in range(i,len(var_name)+i):
                            parse_array[0][j] = ''
                            parse_array[1][j] = -1
                        # Insert the new value
                        parse_array[0][i] = self.env_vars[var_name]
                        parse_array[1][i] = 2
            elif ((c == '~') and (parse_array[1][i] == 0)):
                # Unquoted ~ detected, make sure it's dir-ish
                if ((i == 0) and (len(parse_array[0]) == 1)):
                    # Tilde by itself
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
                elif ((i == 0) and ((parse_array[0][i+1] == '/') or ((parse_array[0][i+1] == ' ') and (parse_array[1][i+1] == 0)))):
                    # Tilde at start, followed by slash or non-escaped space
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
                elif ((len(parse_array[0]) == (i+1)) and ((parse_array[0][i-1] == ' ') and (parse_array[1][i-1] == 0))):
                    # Tilde at end, preceded by a non-escaped space
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
                elif (((parse_array[0][i-1] == ' ') and (parse_array[1][i-1] == 0)) and ((parse_array[0][i+1] == '/') or ((parse_array[0][i+1] == ' ') and (parse_array[1][i+1] == 0)))):
                    # Tilde not at start or end, preceded by a non-escaped space and followed by slash or non-escaped space
                    parse_array[0][i] = self.env_vars.get('$HOME', '/')
                    parse_array[1][i] = 2
        # Stage 2.5: Rebuild the parse array, finalizing expansions
        temp_array = [[],[]]
        for i,c in enumerate(parse_array[0]):
            if (parse_array[1][i] == 2):
                for d in c:
                    temp_array[0].append(d)
                    temp_array[1].append(1)
            elif (parse_array[1][i] >= 0):
                temp_array[0].append(c)
                temp_array[1].append(parse_array[1][i] + 0)
        parse_array = temp_array
        # Stage 2.7: Wildcard globbing
        temp_groups = [[],[]]
        split_mode = 0
        for i,c in enumerate(parse_array[0]):
            # Pre-split into words based on non-escaped whitespace
            if (not ((c in ' \t\n\r') and (parse_array[1][i] == 0))):
                if (split_mode == 0):
                    split_mode = 1
                    temp_groups[0].append([c])
                    temp_groups[1].append([0 + parse_array[1][i]])
                else:
                    temp_groups[0][-1].append(c)
                    temp_groups[1][-1].append(parse_array[1][i])
            else:
                split_mode = 0
                temp_groups[0].append([c])
                temp_groups[1].append([0 + parse_array[1][i]])
        temp_array = [[],[]]
        seen_first = False
        not_whitespace = False
        for i,chunk in enumerate(temp_groups[0]):
            # Iterate through words looking for unescaped glob characters
            glob_chunk = False
            for j,c in enumerate(chunk):
                if ((c in '*[]?') and (temp_groups[1][i][j] == 0)):
                    # Found a chunk with unescaped glob character, but it's not the first chunk
                    if (seen_first):
                        glob_chunk = True
                if (not seen_first):
                    if (not ((c in ' \t\n\r') and (temp_groups[1][i][j] == 0))):
                        not_whitespace = True
            if (not_whitespace):
                seen_first = True
                not_whitespace = False
            if (glob_chunk):
                # Found a glob containing chunk
                glob_str = ''.join(chunk)
                matches = glob.glob(glob_str)
                if (matches):
                    for match in matches:
                        for c in match:
                            temp_array[0].append(c)
                            temp_array[1].append(1)
                        temp_array[0].append(' ')
                        temp_array[1].append(0)
                    _ = temp_array[0].pop()
                    _ = temp_array[1].pop()
                else:
                    for j,c in enumerate(chunk):
                        temp_array[0].append(c)
                        temp_array[1].append(temp_groups[1][i][j])
            else:
                for j,c in enumerate(chunk):
                    temp_array[0].append(c)
                    temp_array[1].append(temp_groups[1][i][j])
        parse_array = temp_array
        # Stage 2.9: Rebuild the parse array, escaping remaining non-whitespace
        temp_array = [[],[]]
        for i,c in enumerate(parse_array[0]):
            if ((c not in ' \t\n\r') and (parse_array[1][i] == 0)):
                temp_array[0].append(c)
                temp_array[1].append(1)
            else:
                temp_array[0].append(c)
                temp_array[1].append(parse_array[1][i] + 0)
        parse_array = temp_array
        # Stage 3: Splitting
        split_mode = 0
        final_value = []
        for i,c in enumerate(parse_array[0]):
            if (parse_array[1][i] == 1):
                if (split_mode == 0):
                    split_mode = 1
                    final_value.append('' + c)
                else:
                    final_value[-1] += c
            else:
                split_mode = 0
        return final_value

class Shell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self._bash = BetterParser()
        self._bash.env_vars['$HOME']   = os.path.expanduser('~/Documents')
        self.did_quit = False
    def bash(self, argstr):
        try:
            return self._bash.parse('. ' + argstr)[1:]
        except SyntaxError as e:
            print("Syntax Error: %s" % e)
            return None
    def pprint(self, path):
        if (path.startswith(self._bash.env_vars['$HOME'])):
            return '~' + path.split(self._bash.env_vars['$HOME'],1)[-1]
        return path
    def do_pwd(self, line):
        """return working directory name"""
        print(self.pprint(os.getcwd()))
    def do_cd(self, line):
        """change the current directory to DIR"""
        args = self.bash(line)
        if args is None:
            return
        elif args and len(args) == 1:
            try:
                os.chdir(args[0])
            except Exception:
                print("cd: %s: No such directory" % line)
        elif len(args) > 1:
            print("cd: Too many arguments")
        else:
            os.chdir(self._bash.env_vars['$HOME'])
    def sizeof_fmt(self, num):
        for x in ['bytes','KB','MB','GB']:
            if num < 1024.0:
                if (x == 'bytes'):
                    return "%s %s" % (num, x)
                else:
                    return "%3.1f %s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')
    def do_mkdir(self, line):
        """make a directory"""
        args = self.bash(line)
        if args is None:
            return
        elif (len(args) == 1):
            target = args[0]
            if os.path.exists(target):
                print("mkdir: %s: File exists" % line)
            else:
                try:
                    os.mkdir(target)
                except Exception:
                    print("mkdir: %s: Unable to create" % line)
        else:
            print("mkdir: Usage: mkdir directory_name")
    def do_mv(self, line):
        """move files and directories"""
        args = self.bash(line)
        if args is None:
            return
        elif (not (len(args) >= 2)):
            print("mv: Usage: mv src [..] dest")
        else:
            dest  = args[-1]
            files = args[0:-1]
            if (len(files) > 1):
                # Moving multiple files, destination must be an existing directory.
                if (not os.path.isdir(dest)):
                    print("cp: %s: No such directory" % self.pprint(dest))
                else:
                    full_dest = os.path.abspath(dest).rstrip('/') + '/'
                    for filef in files:
                        full_file = os.path.abspath(filef).rstrip('/')
                        file_name = os.path.basename(full_file)
                        new_name  = os.path.join(full_dest,file_name)
                        if (not os.path.exists(full_file)):
                            print("! Error: Skipped, missing -", self.pprint(filef))
                            continue
                        try:
                            os.rename(full_file,new_name)
                        except Exception:
                            print("mv: %s: Unable to move" % self.pprint(filef))
            else:
                # Moving a single file to a (pre-existing) directory or a file
                filef = files[0]
                full_file = os.path.abspath(filef).rstrip('/')
                file_name = os.path.basename(full_file)
                full_dest = os.path.abspath(dest).rstrip('/')
                if (os.path.isdir(full_dest)):
                    if (os.path.exists(full_file)):
                        try:
                            os.rename(full_file, full_dest + '/' + file_name)
                        except:
                            print("mv: %s: Unable to move" % self.pprint(filef))
                    else:
                        print("mv: %s: No such file" % self.pprint(filef))
                else:
                    if (os.path.exists(full_file)):
                        try:
                            os.rename(full_file, full_dest)
                        except:
                            print("mv: %s: Unable to move" % self.pprint(filef))
                    else:
                        print("mv: %s: No such file" % self.pprint(filef))
    def do_cp(self, line):
        """copy files and directories"""
        args = self.bash(line)
        if args is None:
            return
        elif (not (len(args) >= 2)):
            print("cp: Usage: cp src [..] dest")
        else:
            if len(args) > 2:
                files = args[:-1]
                dest = args[-1]
            else:
                files = args[:1]
                dest = args[-1]
            if (len(files) > 1):
                # Copying multiple files, destination must be an existing directory.
                if (not os.path.isdir(dest)):
                    print("cp: %s: No such directory" % self.pprint(dest))
                else:
                    full_dest = os.path.abspath(dest).rstrip('/') + '/'
                    for filef in files:
                        full_file = os.path.abspath(filef).rstrip('/')
                        file_name = os.path.basename(full_file)
                        new_name  = os.path.join(full_dest,file_name)
                        if (not os.path.exists(full_file)):
                            print("! Error: Skipped, missing -", self.pprint(filef))
                            continue
                        try:
                            if (os.path.isdir(full_file)):
                                shutil.copytree(full_file,new_name)
                            else:
                                shutil.copy(full_file,new_name)
                        except Exception:
                            print("cp: %s: Unable to copy" % self.pprint(filef))
            else:
                # Copying a single file to a (pre-existing) directory or a file
                filef = files[0]
                full_file = os.path.abspath(filef).rstrip('/')
                file_name = os.path.basename(full_file)
                full_dest = os.path.abspath(dest).rstrip('/')
                new_name = os.path.join(full_dest,file_name)
                if (os.path.isdir(full_dest)):
                    # Destination is a directory already
                    if (os.path.exists(full_file)):
                        try:
                            if (os.path.isdir(full_file)):
                                shutil.copytree(full_file,new_name)
                            else:
                                shutil.copy(full_file,new_name)
                        except:
                            print("cp: %s: Unable to copy" % self.pprint(filef))
                    else:
                        print("cp: %s: No such file" % self.pprint(filef))
                elif (os.path.exists(full_dest)):
                    # Destination is a file
                    if (os.path.exists(full_file)):
                        try:
                            shutil.copy(full_file,full_dest)
                        except:
                            print("cp: %s: Unable to copy" % self.pprint(filef))
                    else:
                        print("cp: %s: No such file" % self.pprint(filef))
                else:
                    if (os.path.isdir(full_file)):
                        # Source is a directory, destination should become a directory
                        try:
                            shutil.copytree(full_file,full_dest)
                        except:
                            print("cp: %s: Unable to copy" % self.pprint(filef))
                    else:
                        # Source is a file, destination should become a file
                        try:
                            shutil.copy(full_file,full_dest)
                        except:
                            print("cp: %s: Unable to copy" % self.pprint(filef))

    def do_rm(self, line):
        """remove one or more files/directories"""
        args = self.bash(line)
        if args is None:
            return
        elif (len(args) < 1):
            print("rm: Usage: rm file_or_dir [...]")
        else:
            for filef in args:
                full_file = os.path.abspath(filef).rstrip('/')
                if not os.path.exists(filef):
                    print("! Skipping: Not found -", self.pprint(filef))
                    continue
                if (os.path.isdir(full_file)):
                    try:
                        shutil.rmtree(full_file, True)
                        if (os.path.exists(full_file)):
                            print("rm: %s: Unable to remove" % self.pprint(filef))
                    except Exception:
                        print("rm: %s: Unable to remove" % self.pprint(filef))
                else:
                    try:
                        os.remove(full_file)
                    except Exception:
                        print("rm: %s: Unable to remove" % self.pprint(filef))
    def do_cat(self, line):
        """print file"""
        args = self.bash(line)
        if args is None:
            return
        elif (len(args) != 1):
            print("cat: Usage: cat file")
        else:
            target = args[0]
            if (not os.path.exists(target)):
                print("cat: %s: No such file" % line)
            elif (os.path.isdir(target)):
                print("cat: %s: Is a directory" % line)
            else:
                try:
                    contents = ""
                    with open(target, 'r') as f:
                        contents = f.read()
                    print(contents)
                    print("")
                except Exception:
                    print("cat: %s: Unable to access" % line)
    def do_ls(self, line):
        """list directory contents"""
        files = self.bash(line)
        if files is None:
            return
        elif (not files):
            files = ['.']
        files_for_path = dict()
        for filef in files:
            full_file = os.path.abspath(filef).rstrip('/')
            file_name = os.path.basename(full_file)
            dir_name  = os.path.dirname(full_file).rstrip('/')
            if (not os.path.exists(full_file)):
                print("! Error: Skipped, missing -", self.pprint(filef))
                continue
            if (os.path.isdir(full_file)):
                # Need to add this as a key and all the files contained inside it
                _dirs = files_for_path.get(full_file, set())
                for new_file in os.listdir(full_file):
                    _dirs.add(full_file.rstrip('/') + '/' + new_file.rstrip('/'))
                files_for_path[full_file] = _dirs
            else:
                _dirs = files_for_path.get(dir_name, set())
                _dirs.add(full_file)
                files_for_path[dir_name] = _dirs
        # Iterate over the paths, in alphabetical order:
        paths = sorted(files_for_path.keys())
        cwd = os.getcwd().rstrip('/')
        in_cwd = False
        if (cwd in paths):
            # Move cwd to the front, mark that it's present
            paths.remove(cwd)
            paths = [cwd] + paths
            in_cwd = True
        for i,path in enumerate(paths):
            if (i > 0):
                print("\n" + self.pprint(path) + "/:")
            elif (not in_cwd):
                print(self.pprint(path) + "/:")
            for filef in sorted(list(files_for_path[path])):
                full_file = os.path.abspath(filef).rstrip('/')
                file_name = os.path.basename(full_file)
                if (os.path.isdir(full_file)):
                    print(file_name + "/")
                else:
                    print(file_name + (" (%s)" % (self.sizeof_fmt(os.stat(full_file).st_size))))
    def do_unzip(self, line):
        """unzip a zip archive"""
        # filename with optional destination
        args = self.bash(line)
        if args is None:
            return
        elif not (1 <= len(args) <= 2):
            print("unzip: Usage: unzip file [destination]")
        else:
            filename = os.path.abspath(args[0])
            if not os.path.isfile(filename):
                print("unzip: %s: No such file" % args[0])
            else:
                # PK magic marker check
                f = open(filename)
                try:
                    pk_check = f.read(2)
                except Exception:
                    pk_check = ''
                finally:
                    f.close()
                if pk_check != 'PK':
                    print("unzip: %s: does not appear to be a zip file" % args[0])
                else:
                    if (os.path.basename(filename).lower().endswith('.zip')):
                        altpath = os.path.splitext(os.path.basename(filename))[0]
                    else:
                        altpath = os.path.basename(filename) + '_unzipped'
                    altpath = os.path.join(os.path.dirname(filename), altpath)
                    location = (args[1:2] or [altpath])[0]
                    if (os.path.exists(location)) and not (os.path.isdir(location)):
                        print("unzip: %s: destination is not a directory" % location)
                        return
                    elif not os.path.exists(location):
                        os.makedirs(location)
                    zipfp = open(filename, 'rb')
                    try:
                        zipf = zipfile.ZipFile(zipfp)
                        # check for a leading directory common to all files and remove it
                        dirnames = [os.path.join(os.path.dirname(x), '') for x in zipf.namelist()]
                        common_dir = os.path.commonprefix(dirnames or ['/'])
                        # Check to make sure there aren't 2 or more sub directories with the same prefix
                        if not common_dir.endswith('/'):
                            common_dir = os.path.join(os.path.dirname(common_dir), '')
                        for name in zipf.namelist():
                            data = zipf.read(name)
                            fn = name
                            if common_dir:
                                if fn.startswith(common_dir):
                                    fn = fn.split(common_dir, 1)[-1]
                                elif fn.startswith('/' + common_dir):
                                    fn = fn.split('/' + common_dir, 1)[-1]
                            fn = fn.lstrip('/')
                            fn = os.path.join(location, fn)
                            dirf = os.path.dirname(fn)
                            if not os.path.exists(dirf):
                                os.makedirs(dirf)
                            if fn.endswith('/'):
                                # A directory
                                if not os.path.exists(fn):
                                    os.makedirs(fn)
                            else:
                                fp = open(fn, 'wb')
                                try:
                                    fp.write(data)
                                finally:
                                    fp.close()
                    except Exception:
                        zipfp.close()
                        print("unzip: %s: zip file is corrupt" % args[0])
                        return
                    finally:
                        zipfp.close()
    def do_untar(self, line):
        """untar a tar archive"""
        # filename with optional destination
        args = self.bash(line)
        if args is None:
            return
        elif not (1 <= len(args) <= 2):
            print("untar: Usage: untar file [destination]")
        else:
            filename = os.path.abspath(args[0])
            if not os.path.isfile(filename):
                print("untar: %s: No such file" % args[0])
            else:
                # 'ustar' magic marker check
                f = open(filename)
                try:
                    f.seek(257)
                    ustar_check = f.read(5)
                except Exception:
                    ustar_check = ''
                finally:
                    f.close()
                if ustar_check != 'ustar':
                    print("untar: %s: does not appear to be a tar file" % args[0])
                else:
                    if (os.path.basename(filename).lower().endswith('.tar')):
                        altpath = os.path.splitext(os.path.basename(filename))[0]
                    else:
                        altpath = os.path.basename(filename) + '_untarred'
                    altpath = os.path.join(os.path.dirname(filename), altpath)
                    location = (args[1:2] or [altpath])[0]
                    if (os.path.exists(location)) and not (os.path.isdir(location)):
                        print("untar: %s: destination is not a directory" % location)
                        return
                    elif not os.path.exists(location):
                        os.makedirs(location)
                    try:
                        tar = tarfile.open(filename, 'r')
                        # check for a leading directory common to all files and remove it
                        dirnames = [os.path.join(os.path.dirname(x.name), '') for x in tar.getmembers() if x.name != 'pax_global_header']
                        common_dir = os.path.commonprefix(dirnames or ['/'])
                        if not common_dir.endswith('/'):
                            common_dir = os.path.join(os.path.dirname(common_dir), '')
                        for member in tar.getmembers():
                            fn = member.name
                            if fn == 'pax_global_header':
                                continue
                            if common_dir:
                                if fn.startswith(common_dir):
                                    fn = fn.split(common_dir, 1)[-1]
                                elif fn.startswith('/' + common_dir):
                                    fn = fn.split('/' + common_dir, 1)[-1]
                            fn = fn.lstrip('/')
                            fn = os.path.join(location, fn)
                            dirf = os.path.dirname(fn)
                            if member.isdir():
                                # A directory
                                if not os.path.exists(fn):
                                    os.makedirs(fn)
                            elif member.issym():
                                # skip symlinks
                                continue
                            else:
                                try:
                                    fp = tar.extractfile(member)
                                except (KeyError, AttributeError):
                                    # invalid member, not necessarily a bad tar file
                                    continue
                                if not os.path.exists(dirf):
                                    os.makedirs(dirf)
                                with open(fn, 'wb') as destfp:
                                    shutil.copyfileobj(fp, destfp)
                                fp.close()
                    except Exception:
                        tar.close()
                        print("untar: %s: tar file is corrupt" % args[0])
                        return
                    finally:
                        tar.close()
    def do_ungzip(self, line, gunzip=False):
        """ungzip a gzip archive"""
        # filename with optional output filename
        fname = 'ungzip'
        if gunzip:
            fname = 'gunzip'
        args = self.bash(line)
        if args is None:
            return
        elif not (1 <= len(args) <= 2):
            print("%s: Usage: %s file [outfile]" % (fname, fname))
        else:
            filename = os.path.abspath(args[0])
            if not os.path.isfile(filename):
                print("%s: %s: No such file" % (fname,args[0]))
            else:
                # '\x1f\x8b\x08' magic marker check
                f = open(filename, 'rb')
                try:
                    gz_check = f.read(3)
                except Exception:
                    gz_check = ''
                finally:
                    f.close()
                if gz_check != '\x1f\x8b\x08':
                    print("%s: %s: does not appear to be a gzip file" % (fname,args[0]))
                else:
                    if (os.path.basename(filename).lower().endswith('.gz') or os.path.basename(filename).lower().endswith('.gzip')):
                        altpath = os.path.splitext(os.path.basename(filename))[0]
                    elif os.path.basename(filename).lower().endswith('.tgz'):
                        altpath = os.path.splitext(os.path.basename(filename))[0] + '.tar'
                    else:
                        altpath = os.path.basename(filename) + '_ungzipped'
                    altpath = os.path.join(os.path.dirname(filename), altpath)
                    location = (args[1:2] or [altpath])[0]
                    if os.path.exists(location):
                        print("%s: %s: destination already exists" % (fname,os.path.basename(location)))
                        return                    
                    dirf = os.path.dirname(os.path.dirname(os.path.abspath(location)))
                    try:
                        if not os.path.exists(dirf):
                            os.makedirs(dirf)
                        with open(location, 'wb') as outfile:
                            with gzip.open(filename, 'rb') as gzfile:
                                outfile.write(gzfile.read())
                    except Exception:
                        print("%s: %s: gzip file is corrupt" % (fname, args[0]))
    def do_gunzip(self, line):
        """ungzip a gzip archive"""
        self.do_ungzip(line, gunzip=True)
    def do_quit(self,line):
        self.did_quit = True
    def do_q(self,line):
        self.did_quit = True
    def do_exit(self,line):
        self.did_quit = True
    def do_logout(self,line):
        self.did_quit = True
    def do_logoff(self,line):
        self.did_quit = True
    def postcmd(self,stop,line):
        return self.did_quit

def main():
    shell = Shell()
    shell.prompt = '> '
    shell.cmdloop()

if __name__ == '__main__':
    main()