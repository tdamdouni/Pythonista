import os, cmd, sys, glob, os.path, shutil, zipfile, tarfile, gzip, urllib2, traceback, getpass

try:
	import ui
except ImportError:
	print "Continuing without UI module (possibly not running on iPad)"

#Option to install required modules as a subdirectory of the shellista.py module
#or install in the user site-packages folder.
LOCAL_SITE_PACKAGES=True

# Credits
#
# The python code here was written by pudquick@github
#
# License
#
# This code is released under a standard MIT license.
#
#   Permission is hereby granted, free of charge, to any person
#   obtaining a copy of this software and associated documentation files
#   (the "Software"), to deal in the Software without restriction,
#   including without limitation the rights to use, copy, modify, merge,
#   publish, distribute, sublicense, and/or sell copies of the Software,
#   and to permit persons to whom the Software is furnished to do so,
#   subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
#   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
#   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

# You can skip over reading this class, if you like.
# It's an implementation of mine of the bash parser in pure python
# This has advantages over shlex, glob, and shlex->glob in that it expects
# the strings to represent files from the start.

#Modified by transistor1 (svrusso1 - at - gmail - dot - com):
# - Integrate minimal pipista functionality
#  - pdown - PyPi download
#  - psrch - PyPi search
# - Minimal Git functionality
#  - git init - Initialize git repo
#  - git add - Stage one or more files
#  - git commit - Commit staged files
#  - git clone - clone a public repo (no auth)
#  - git push - push commits via web
#  - git modified - see which files are currently modified
#  - git log - doesn't currently work
# - untgz - a convenience wrapper to untar and ungzip at the same time
#  - Also ripped @mark_tully's wget - thanks Mark!
# - Simple Python sub-shell by typing 'shell', 'python', or '!'
#  - Running a file directly doesn't work (e.g. 'python somefile.py'), though I tried
#  - Single-line commands only



PIPISTA_URL='https://gist.githubusercontent.com/transistor1/0ea245e666189b3e675a/raw/23a23e229d6c279be3bc380c18c22fc2de24ef17/pipista.py'
DULWICH_URL='https://github.com/transistor1/dulwich/archive/master.tar.gz'
GITTLE_URL='https://github.com/FriendCode/gittle/archive/522ce011851aee28fd6bb11b502978c9352fd137.tar.gz'
FUNKY_URL='https://github.com/FriendCode/funky/tarball/e89cb2ce4374bf2069c7f669e52e046f63757241#egg=funky-0.0.1'
MIMER_URL='https://github.com/FriendCode/mimer/tarball/a812e5f631b9b5c969df5a2ea84b635490a96ced#egg=mimer-0.0.1'

if LOCAL_SITE_PACKAGES:
	module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local-packages')
else:
	import site
	module_dir = site.USER_SITE

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

class PyShell(cmd.Cmd):
	def __init__(self):
				#super(PyShell, self).__init__()
		cmd.Cmd.__init__(self)
		self.did_quit = False
		self.exec_globals = globals()
		self.exec_locals = {}
	def do_quit(self, NoParams=None):
		"""exit shell"""
		self.did_quit = True
	def emptyline(self):
		pass
	def precmd(self,line):
		if not line.startswith('quit'):
			if line:
				try:
					exec(line,self.exec_globals,self.exec_locals)
				except SyntaxError as e:
					print 'Syntax Error: {0}'.format(e)
				except ImportError as e:
					print 'Import Error: {0}'.format(e)
				except NameError as e:
					print 'Name Error: {0}'.format(e)
				except:
					print 'Error: {0}'.format(sys.exc_value)
			return '\n'
		else:
			return cmd.Cmd.precmd(self,line)
	def postcmd(self,stop,line):
		return self.did_quit

class Shell(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self._bash = BetterParser()
		self._bash.env_vars['$HOME']   = os.path.expanduser('~/Documents')
		self.did_quit = False
	def bash(self, argstr):
		try:
			return self._bash.parse('. ' + argstr)[1:]
		except SyntaxError, e:
			print "Syntax Error: %s" % e
			return None
	def pprint(self, path):
		if (path.startswith(self._bash.env_vars['$HOME'])):
			return '~' + path.split(self._bash.env_vars['$HOME'],1)[-1]
		return path
	#WGet clone by Mark Tully - https://gist.github.com/mctully/4367145
	def do_wget(self,line):
		"""WGet clone
		wget: usage "wget URL [optional output filename]"
		"""
		args=self.bash(line)
		if len(args)<1 or len(args)>2:
			print 'wget: usage "wget URL [optional output filename]"'
		else:
			self.wget(args)

	def wget(self, args):
		import urllib2,contextlib
		url=args[0]
		dst=args[1] if len(args)>1 else os.path.basename(url.split('?',1)[0])
		print 'Downloading to "%s"'%dst
		try:
			total=0
			with contextlib.closing(urllib2.urlopen(url)) as c:
				with open(dst,'wb') as f:
					while True:
						data=c.read(32*1024)
						if data=='':
							break
						f.write(data)
						total+=len(data)
						print 'downloaded %d bytes'%total
		except Exception as e:
			print 'wget: error',e

	def do_git(self,line):
		"""Very basic Git commands: init, stage, commit, clone, modified, branch"""
		from gittle import Gittle
		
		#TODO: These git functions all follow the same pattern.
		#Refactor these so they only contain their unique logic

		#TODO: If there is no ~/.gitconfig file, set up the username and password

		self.git_user = None
		self.git_email = None

		def git_init(args):
			if len(args) == 1:
				Gittle.init(args[0])
			else:
				print command_help['init']
		
		
		def git_status(args):
			if len(args) == 0:
				repo = Gittle('.')
				status = porcelain.status(repo.repo)
				print status

				#repo.diff_working()
				#repo.diff(diff_type='changes')
				#print repo.modified_files.intersection(repo.added_files) #repo.tracked_files.intersection(repo.added_files)
				#print repo.added_files
			else:
				print command_help['git_staged']

		def git_remote(args):
			'''List remote repos'''
			if len(args) == 0:
				repo = Gittle('.')
				for key, value in repo.remotes.items():
					print key, value
			else:
				print command_help['remote']

		def git_add(args):
			if len(args) > 0:
				repo = Gittle('.')
				repo.stage(args)
			else:
				print command_help['add']
				
		def git_rm(args):
			if len(args) > 0:
				repo = Gittle('.')
				repo.rm(args)
			else:
				print command_help['rm']

		def git_branch(args):
			if len(args) == 0:
				repo = Gittle('.')
				active = repo.active_branch
				for key, value in repo.branches.items():
					print ('* ' if key == active else '') + key, value
			else:
				print command_help['branch']

		def git_commit(args):
			if len(args) == 3:
				try:
					repo = Gittle('.')
					print repo.commit(name=args[1],email=args[2],message=args[0])
				except:
					print 'Error: {0}'.format(sys.exc_value)
			else:
				print command_help['commit']

		def git_clone(args):
			if len(args) > 0:
				url = args[0]

				#def clone(source, target=None, bare=False, checkout=None, config=None, opener=None, outstream=sys.stdout):
				repo = Gittle.clone(args[0], args[1] if len(args)>1 else '.', bare=False)

				#porcelain.clone(url, target='.')
				#repo = Gittle('.')

				#Set the origin
				config = repo.repo.get_config()
				config.set(('remote','origin'),'url',url)
				config.write_to_path()
			else:
				print command_help['clone']

		def git_pull(args):
			if len(args) <= 1:
				repo = Gittle('.')
				url = args[0] if len(args)==1 else repo.remotes.get('origin','')
				if url:
					repo.pull(origin_uri=url)
				else:
					print 'No pull URL.'
			else:
				print command_help['git pull']
				
				
				
		def git_push(args):
			import argparse
			parser = argparse.ArgumentParser(prog='git push'
											 , usage='git push [http(s)://<remote repo>] [-u username[:password]]'
											 , description="Push to a remote repository")
			parser.add_argument('url', type=str, nargs='?', help='URL to push to')
			parser.add_argument('-u', metavar='username[:password]', type=str, required=False, help='username[:password]')
			result = parser.parse_args(args)

			user, sep, pw = result.u.partition(':') if result.u else (None,None,None)

			repo = Gittle('.')

			#Try to get the remote origin
			if not result.url:
				result.url = repo.remotes.get('origin','')

			branch_name = os.path.join('refs','heads', repo.active_branch)  #'refs/heads/%s' % repo.active_branch

			print "Attempting to push to: {0}, branch: {1}".format(result.url, branch_name)

			if user:
				if not pw:
					pw = getpass.getpass('Enter password for {0}: '.format(user))

				opener = auth_urllib2_opener(None, result.url, user, pw)

				print porcelain.push(repo.repo, result.url, branch_name, opener=opener)
			else:
				print porcelain.push(repo.repo, result.url, branch_name)

		def git_modified(args):
			repo = Gittle('.')
			for mod_file in repo.modified_files:
				print mod_file

		def git_log(args):
			if len(args) <= 1:
				try:
					porcelain.log(max_entries=int(args[0]) if len(args)==1 else None)
				except ValueError:
					print command_help['log']
			else:
				print command_help['log']

#    def switch_branch(self, branch_name, tracking=None, create=None):
		def git_checkout(args):
			if len(args) == 1:
				repo = Gittle('.')
				repo.clean_working()
				#repo.checkout('refs/heads/{0}'.format(args[0]))
				repo.switch_branch('{0}'.format(args[0]))
			else:
				print command_help['checkout']

		def git_help(args):
			print 'help:'
			for key, value in command_help.items():
				print value

		#TODO: Alphabetize
		commands = {
		'init': git_init
		,'add': git_add
		,'rm': git_rm
		,'commit': git_commit
		,'clone': git_clone
		,'modified': git_modified
		,'log': git_log
		,'push': git_push
		,'pull': git_pull
		,'branch': git_branch
		,'checkout': git_checkout
		,'remote': git_remote
		,'status': git_status
		,'help': git_help
		}

		command_help = {
		'init':  'git init <directory> - initialize a new Git repository'
		,'add': 'git add <file1> .. [file2] .. - stage one or more files'
		,'rm': 'git rm <file1> .. [file2] .. - git rm one or more files'
		,'commit': 'git commit <message> <name> <email> - commit staged files'
		,'clone': 'git clone <url> [path] - clone a remote repository'
		,'modified': 'git modified - show what files have been modified'
		,'log': 'git log [number of changes to show] - show a full log of changes'
		,'push': 'git push [http(s)://<remote repo>] [-u username[:password]] - push changes back to remote'
		,'pull': 'git pull [http(s)://<remote repo>] - pull changes from a remote repository'
		,'checkout': 'git checkout <branch> - check out a particular branch in the Git tree'
		,'branch': 'git branch - show branches'
		,'status': 'git status - show status of files (staged, unstaged, untracked)'
		,'help': 'git help'
		}

		#git_init.__repr__ = "git init abc"

		args = self.bash(line)

		try:
			#Call the command and pass args
			cmd = commands.get(args[0] if len(args) > 0 else 'help','help')
			cmd(args[1:])
		except:
			#import traceback
			#traceback.print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)
			#traceback.print_tb(sys.exc_traceback)
			print 'Error: {0}'.format(sys.exc_value)


	def do_untgz(self, file):
		"""Helper to run both ungzip and untar on a file"""
		result = self.do_ungzip(file, gunzip=True)
		if result:
			self.do_untar(result)
			if os.path.isfile(result):
				self.do_rm(result)
	def do_shell(self, args):
		"""Python shell"""
		self.do_python(args)
	def do_python(self,line):
		"""Python shell"""
		args = self.bash(line)
		#Save the old path, in case user messes with it in shell

		with _save_context():
			sys.path.append(os.getcwd())

			if len(args)==0:
				print 'Entering Python shell'
				p = PyShell()
				p.prompt = '>>> '
				p.cmdloop()
			else:
				#Run the program and pass any args.
				try:
					tmpg = globals()
					tmpl = locals()
					sys.argv = args[:]
					execfile(os.path.join(os.getcwd(),args[0]), tmpg, tmpl)
				except:
					print 'Error: {0}'.format(sys.exc_value)

	def do_pdown(self, modulename):
		"""Download a module from pypi"""
		try:
			pipista.pypi_download(modulename)
		except pipista.PyPiError:
			print 'Module {0} not found.'.format(modulename)

	def do_psrch(self, search_term):
		"""Search PyPi for a module"""
		try:
			results = pipista.pypi_search(search_term)
			#print self.pprint( '{0}'.format(result) )
			print '** Number of results for "{0}" from PyPi: {1}'.format(search_term, len(results))
			for i in xrange(len(results)):
				print '\t** Result {0} of {1}'.format(i + 1, len(results))
				for key, value in results[i].items():
					print '\t\t{0}: {1}'.format(key, value)
		except pipista.PyPiError:
			print 'Couldn\'t find {0}'.format(search_term)
	def do_pwd(self, line):
		"""return working directory name"""
		print self.pprint(os.getcwd())
	def do_cd(self, line):
		"""change the current directory to DIR"""
		args = self.bash(line)
		if args is None:
			return
		elif args and len(args) == 1:
			try:
				os.chdir(args[0])
			except Exception:
				print "cd: %s: No such directory" % line
		elif len(args) > 1:
			print "cd: Too many arguments"
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
				print "mkdir: %s: File exists" % line
			else:
				try:
					os.mkdir(target)
				except Exception:
					print "mkdir: %s: Unable to create" % line
		else:
			print "mkdir: Usage: mkdir directory_name"
	def do_mv(self, line):
		"""move files and directories"""
		args = self.bash(line)
		if args is None:
			return
		elif (not (len(args) >= 2)):
			print "mv: Usage: mv src [..] dest"
		else:
			dest  = args[-1]
			files = args[0:-1]
			if (len(files) > 1):
				# Moving multiple files, destination must be an existing directory.
				if (not os.path.isdir(dest)):
					print "cp: %s: No such directory" % self.pprint(dest)
				else:
					full_dest = os.path.normpath(os.path.abspath(dest)) + '/'
					for filef in files:
						full_file = os.path.normpath(os.path.abspath(filef))
						file_name = os.path.basename(full_file)
						new_name  = os.path.join(full_dest,file_name)
						if (not os.path.exists(full_file)):
							print "! Error: Skipped, missing -", self.pprint(filef)
							continue
						try:
							os.rename(full_file,new_name)
						except Exception:
							print "mv: %s: Unable to move" % self.pprint(filef)
			else:
				# Moving a single file to a (pre-existing) directory or a file
				filef = files[0]
				full_file = os.path.normpath(os.path.abspath(filef))
				file_name = os.path.basename(full_file)
				full_dest = os.path.normpath(os.path.abspath(dest))
				if (os.path.isdir(full_dest)):
					if (os.path.exists(full_file)):
						try:
							os.rename(full_file, full_dest + '/' + file_name)
						except:
							print "mv: %s: Unable to move" % self.pprint(filef)
					else:
						print "mv: %s: No such file" % self.pprint(filef)
				else:
					if (os.path.exists(full_file)):
						try:
							os.rename(full_file, full_dest)
						except:
							print "mv: %s: Unable to move" % self.pprint(filef)
					else:
						print "mv: %s: No such file" % self.pprint(filef)
	def do_cp(self, line):
		"""copy files and directories"""
		args = self.bash(line)
		if args is None:
			return
		elif (not (len(args) >= 2)):
			print "cp: Usage: cp src [..] dest"
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
					print "cp: %s: No such directory" % self.pprint(dest)
				else:
					full_dest = os.path.normpath(os.path.abspath(dest)) + '/'
					for filef in files:
						full_file = os.path.normpath(os.path.abspath(filef))
						file_name = os.path.basename(full_file)
						new_name  = os.path.join(full_dest,file_name)
						if (not os.path.exists(full_file)):
							print "! Error: Skipped, missing -", self.pprint(filef)
							continue
						try:
							if (os.path.isdir(full_file)):
								shutil.copytree(full_file,new_name)
							else:
								shutil.copy(full_file,new_name)
						except Exception:
							print "cp: %s: Unable to copy" % self.pprint(filef)
			else:
				# Copying a single file to a (pre-existing) directory or a file
				filef = files[0]
				full_file = os.path.normpath(os.path.abspath(filef))
				file_name = os.path.basename(full_file)
				full_dest = os.path.normpath(os.path.abspath(dest))
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
							print "cp: %s: Unable to copy" % self.pprint(filef)
					else:
						print "cp: %s: No such file" % self.pprint(filef)
				elif (os.path.exists(full_dest)):
					# Destination is a file
					if (os.path.exists(full_file)):
						try:
							shutil.copy(full_file,full_dest)
						except:
							print "cp: %s: Unable to copy" % self.pprint(filef)
					else:
						print "cp: %s: No such file" % self.pprint(filef)
				else:
					if (os.path.isdir(full_file)):
						# Source is a directory, destination should become a directory
						try:
							shutil.copytree(full_file,full_dest)
						except:
							print "cp: %s: Unable to copy" % self.pprint(filef)
					else:
						# Source is a file, destination should become a file
						try:
							shutil.copy(full_file,full_dest)
						except:
							print "cp: %s: Unable to copy" % self.pprint(filef)

	def do_rm(self, line):
		"""remove one or more files/directories"""
		args = self.bash(line)
		if args is None:
			return
		elif (len(args) < 1):
			print "rm: Usage: rm file_or_dir [...]"
		else:
			for filef in args:
				full_file = os.path.normpath(os.path.abspath(filef))
				if not os.path.exists(filef):
					print "! Skipping: Not found -", self.pprint(filef)
					continue
				if (os.path.isdir(full_file)):
					try:
						shutil.rmtree(full_file, True)
						if (os.path.exists(full_file)):
							print "rm: %s: Unable to remove" % self.pprint(filef)
					except Exception:
						print "rm: %s: Unable to remove" % self.pprint(filef)
				else:
					try:
						os.remove(full_file)
					except Exception:
						print "rm: %s: Unable to remove" % self.pprint(filef)
	def do_cat(self, line):
		"""print file"""
		args = self.bash(line)
		if args is None:
			return
		elif (len(args) != 1):
			print "cat: Usage: cat file"
		else:
			target = args[0]
			if (not os.path.exists(target)):
				print "cat: %s: No such file" % line
			elif (os.path.isdir(target)):
				print "cat: %s: Is a directory" % line
			else:
				try:
					contents = ""
					with open(target, 'r') as f:
						contents = f.read()
					print contents
					print ""
				except Exception:
					print "cat: %s: Unable to access" % line
	def do_ls(self, line):
		"""list directory contents"""
		files = self.bash(line)
		if files is None:
			return
		elif (not files):
			files = ['.']
		files_for_path = dict()
		for filef in files:
			full_file = os.path.normpath(os.path.abspath(filef))
			file_name = os.path.basename(full_file)
			dir_name  = os.path.normpath(os.path.dirname(full_file))
			if (not os.path.exists(full_file)):
				print "! Error: Skipped, missing -", self.pprint(filef)
				continue
			if (os.path.isdir(full_file)):
				# Need to add this as a key and all the files contained inside it
				_dirs = files_for_path.get(full_file, set())
				for new_file in os.listdir(full_file):
					_dirs.add(os.path.normpath(full_file) + '/' + os.path.normpath(new_file))
				files_for_path[full_file] = _dirs
			else:
				_dirs = files_for_path.get(dir_name, set())
				_dirs.add(full_file)
				files_for_path[dir_name] = _dirs
		# Iterate over the paths, in alphabetical order:
		paths = sorted(files_for_path.keys())
		cwd = os.path.normpath(os.getcwd())
		in_cwd = False
		if (cwd in paths):
			# Move cwd to the front, mark that it's present
			paths.remove(cwd)
			paths = [cwd] + paths
			in_cwd = True
		for i,path in enumerate(paths):
			if (i > 0):
				print "\n" + self.pprint(path) + "/:"
			elif (not in_cwd):
				print self.pprint(path) + "/:"
			for filef in sorted(list(files_for_path[path])):
				full_file = os.path.normpath(os.path.abspath(filef))
				file_name = os.path.basename(full_file)
				if (os.path.isdir(full_file)):
					print file_name + "/"
				else:
					try:
						print file_name + (" (%s)" % (self.sizeof_fmt(os.stat(full_file).st_size)))
					except OSError:
						print file_name + " (OSError)"
	def do_unzip(self, line):
		"""unzip a zip archive"""
		# filename with optional destination
		args = self.bash(line)
		if args is None:
			return
		elif not (1 <= len(args) <= 2):
			print "unzip: Usage: unzip file [destination]"
		else:
			filename = os.path.abspath(args[0])
			if not os.path.isfile(filename):
				print "unzip: %s: No such file" % args[0]
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
					print "unzip: %s: does not appear to be a zip file" % args[0]
				else:
					if (os.path.basename(filename).lower().endswith('.zip')):
						altpath = os.path.splitext(os.path.basename(filename))[0]
					else:
						altpath = os.path.basename(filename) + '_unzipped'
					altpath = os.path.join(os.path.dirname(filename), altpath)
					location = (args[1:2] or [altpath])[0]
					if (os.path.exists(location)) and not (os.path.isdir(location)):
						print "unzip: %s: destination is not a directory" % location
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
						print "unzip: %s: zip file is corrupt" % args[0]
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
			print "untar: Usage: untar file [destination]"
		else:
			filename = os.path.abspath(args[0])
			if not os.path.isfile(filename):
				print "untar: %s: No such file" % args[0]
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
					print "untar: %s: does not appear to be a tar file" % args[0]
				else:
					if (os.path.basename(filename).lower().endswith('.tar')):
						altpath = os.path.splitext(os.path.basename(filename))[0]
					else:
						altpath = os.path.basename(filename) + '_untarred'
					altpath = os.path.join(os.path.dirname(filename), altpath)
					location = (args[1:2] or [altpath])[0]
					if (os.path.exists(location)) and not (os.path.isdir(location)):
						print "untar: %s: destination is not a directory" % location
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
						print "untar: %s: tar file is corrupt" % args[0]
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
			print "%s: Usage: %s file [outfile]" % (fname, fname)
		else:
			filename = os.path.abspath(args[0])
			if not os.path.isfile(filename):
				print "%s: %s: No such file" % (fname,args[0])
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
					print "%s: %s: does not appear to be a gzip file" % (fname,args[0])
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
						print "%s: %s: destination already exists" % (fname,os.path.basename(location))
						return
					dirf = os.path.dirname(os.path.dirname(os.path.abspath(location)))
					try:
						if not os.path.exists(dirf):
							os.makedirs(dirf)
						with open(location, 'wb') as outfile:
							with gzip.open(filename, 'rb') as gzfile:
								outfile.write(gzfile.read())
						return location
					except Exception:
						print "%s: %s: gzip file is corrupt" % (fname, args[0])
	def do_gunzip(self, line):
		"""ungzip a gzip archive"""
		self.do_ungzip(line, gunzip=True)
		
	def do_touch(self, line):
		"""touch a file, either creating it or modifying the modified date"""
		args = self.bash(line)
		if len(args) == 1:
			with open(args[0],'ab+') as f:
				pass
		else:
			print "Couldn't touch file"
			
	def do_quit(self,line):
		"""exit shell"""
		self.did_quit = True
	def do_q(self,line):
		"""exit shell"""
		self.did_quit = True
	def do_exit(self,line):
		"""exit shell"""
		self.did_quit = True
	def do_logout(self,line):
		"""exit shell"""
		self.did_quit = True
	def do_logoff(self,line):
		"""exit shell"""
		self.did_quit = True
	def postcmd(self,stop,line):
		return self.did_quit
	def emptyline(self):
		pass
	def onecmd(self, line):
		try:
			cmd.Cmd.onecmd(self, line)
		except:
			print "Unhandled Exception:"
			traceback.print_exc()
	def precmd(self,line):
		#check if last char is tab, in which case, autocompl
		#If last char is two tabs, nuke last argument
		while line.endswith('    '):
			if line.endswith('        '):
				newline=' '.join([s.replace(' ',"' '") for s in self._bash.parse(line)[:-1]])
			else:
				newline=_tabcompl(line,self._bash)
			line=newline+raw_input('+++' + newline)
		print '>' + line
		return line

def _tabcompl(line,bash):
		"""complete partial line"""
		args=bash.parse(line)
		filef=args[-1]

		full_file = os.path.relpath(filef)
		file_name = os.path.basename(filef)
		dir_name  = os.path.relpath(os.path.normpath(os.path.dirname(filef)))
		files = os.listdir(dir_name)
		matchingfiles = [f for f in files if f.startswith(file_name)]

		table=ui.TableView()
		listsource=ui.ListDataSource(matchingfiles)
		listsource.font=('<system>',10)
		listsource.action=_tapaction
		table.data_source=listsource
		table.delegate=listsource
		table.width=300
		table.height=300
		table.row_height=15
		table.present('popover')
		if len(matchingfiles) > 1:
			table.wait_modal()
		else:
			table.close()
		#now, replace last arg with the match.  
		if len(matchingfiles) > 0:
			args[-1]=os.path.join(dir_name,matchingfiles[table.selected_row[1]])
		else:
			args[-1]=''  #no match... just kill arg
		newline=' '.join([s.replace(' ',"' '") for s in args])
		return newline
def _tapaction(sender):
	sender.tableview.close()


def _global_import(modulename):
	module = __import__(modulename,globals(),locals())
	globals()[modulename]=module

def _import_optional(modulename, url, filename, after_extracted, shellfuncs):
	"""import optional modules, downloading if possible. Disable
	shell functionality if the module can't be loaded."""
	try:
	#os.chdir('~')
		_global_import(modulename)
	except:
		print 'Requires {0} ... attempting to download.'.format(modulename)
		s = Shell()
		#s.do_cd('~')
		s.do_mkdir('.shellista_tmp')
		s.do_cd('.shellista_tmp')
		s.do_wget("{0} {1}".format(url, filename))
		after_extracted(s, os.getcwd(), modulename)
		s.do_cd('..')
		s.do_rm('.shellista_tmp')
		try:
			_global_import(modulename)
		except:
			print 'Error importing {0}, continuing without.'.format(modulename)
			for f in shellfuncs:
				#Delete commands that we can't get dependencies for1
				exec('del Shell.{0}'.format(f), globals(), locals())

def _extract_generic(shell, path, modulename):
	shell.do_untgz('{0}.tar.gz'.format(modulename))
	shell.do_mv('{0}/*/{0} {1}/'.format(modulename, module_dir))

def _extract_pipista(shell, path, modulename):
	shell.do_mv('pipista.py {0}'.format(module_dir))

def _shellista_setup():
	#make sure site-packages is in the path.  If shellista is
	#in a subfolder of ~, it will create a site-packages subfolder
	#so shellista can be installed anywhere.

	if not os.path.exists(module_dir):
		os.mkdir(module_dir)
	
	if not module_dir in sys.path:
		sys.path.insert(0, module_dir + '/')

	
	_import_optional('pipista', PIPISTA_URL, 'pipista.py', _extract_pipista, ['do_psrch','do_pdown'])
	_import_optional('dulwich', DULWICH_URL, 'dulwich.tar.gz', _extract_generic, [])
	_import_optional('funky', FUNKY_URL, 'funky.tar.gz', _extract_generic, [])
	_import_optional('mimer', MIMER_URL, 'mimer.tar.gz', _extract_generic, [])
	_import_optional('gittle', GITTLE_URL, 'gittle.tar.gz', _extract_generic, ['do_git'])
	
_shellista_setup()
if globals().get('dulwich'):
	from dulwich.client import default_user_agent_string
	from dulwich import porcelain

import contextlib
@contextlib.contextmanager
def _save_context():
	sys._argv = sys.argv[:]
	sys._path = sys.path[:]
	yield
	sys.argv = sys._argv
	sys.path = sys._path

#Urllib2 opener for dulwich
def auth_urllib2_opener(config, top_level_url, username, password):
	if config is not None:
		proxy_server = config.get("http", "proxy")
	else:
		proxy_server = None

	# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

		# Add the username and password.
		# If we knew the realm, we could use it instead of None.
		#top_level_url = "http://example.com/foo/"
		password_mgr.add_password(None, top_level_url, username, password)

		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

	handlers = [handler]
	if proxy_server is not None:
		handlers.append(urllib2.ProxyHandler({"http": proxy_server}))
	opener = urllib2.build_opener(*handlers)
	if config is not None:
		user_agent = config.get("http", "useragent")
	else:
		user_agent = None
	if user_agent is None:
		user_agent = default_user_agent_string()
	opener.addheaders = [('User-agent', user_agent)]
	return opener

def main():
	#from gittle import Gittle
	
	#Gittle.push_to = push_to
	
	shell = Shell()
	shell.prompt = '> '
	shell.cmdloop()

if __name__ == '__main__':
	main()

