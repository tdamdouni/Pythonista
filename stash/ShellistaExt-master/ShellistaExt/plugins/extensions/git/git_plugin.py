'''git:
Git commands for Shellista
usage: git help
'''
import os
import sys
import argparse
import urlparse
import urllib2
import getpass

alias = []

from ... tools.toolbox import bash

#iOS-specific
try:
    import console
except:
    from ... tools import ios_console as console

from ... tools import ios_keychain as keychain


shellista = sys.modules['__main__']

SAVE_PASSWORDS = shellista.Shellista.settings.get('save_passwords', True)

__DEBUG__ = False

if __DEBUG__:

    base_url = 'file://' + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + '/shellista-deps'
    DULWICH_URL = base_url + '/dulwich.tar.gz#module_name=dulwich&module_path=dulwich-master/dulwich&move_to=./local-modules'
    GITTLE_URL = base_url + '/gittle.tar.gz#module_name=gittle&module_path=gittle-*/gittle&move_to=./local-modules'
    FUNKY_URL = base_url + '/funky.tar.gz#module_name=funky&module_path=*funky-*/funky&move_to=./local-modules'
    MIMER_URL = base_url + '/mimer.tar.gz#module_name=mimer&module_path=*mimer-*/mimer&move_to=./local-modules'

else:
    #PIPISTA_URL='https://gist.githubusercontent.com/transistor1/0ea245e666189b3e675a/raw/23a23e229d6c279be3bc380c18c22fc2de24ef17/pipista.py#module_name=pipista&module_path=pipista.py&move_to=local-modules'
    DULWICH_URL='https://github.com/transistor1/dulwich/archive/master.tar.gz#module_name=dulwich&module_path=dulwich-master/dulwich&move_to=local-modules'
    GITTLE_URL='https://github.com/FriendCode/gittle/archive/522ce011851aee28fd6bb11b502978c9352fd137.tar.gz#module_name=gittle&module_path=gittle-*/gittle&move_to=local-modules'
    FUNKY_URL='https://github.com/FriendCode/funky/tarball/e89cb2ce4374bf2069c7f669e52e046f63757241#module_name=funky&module_path=Friend*/funky&move_to=local-modules&save_as=funky.tar.gz'
    MIMER_URL='https://github.com/FriendCode/mimer/tarball/a812e5f631b9b5c969df5a2ea84b635490a96ced#module_name=mimer&module_path=Friend*/mimer&move_to=local-modules&save_as=mimer.tar.gz'

def _progress(tot):
    print 'Downloaded {0} bytes'.format(tot)
    
#Make sure you order these in terms of what is needed first
for i in [FUNKY_URL, MIMER_URL, DULWICH_URL, GITTLE_URL]:
    installer = shellista.ModuleInstaller(i, root_dir=os.path.dirname(os.path.abspath(__file__)))
    print "Importing " + installer.module_name
    installer.try_import_or_install(overwrite_existing=True, progress_func=_progress)

#Dulwich imports can now be done, since we've downloaded the modules
from dulwich.client import default_user_agent_string
from dulwich import porcelain
from gittle import Gittle


def main(self, line):
    do_git(line)
    
#TODO: This might be better as a class, play around with it

def do_git(line):
    """Very basic Git commands: init, stage, commit, clone, modified, branch"""
    #TODO: Clean up this code
    #TODO: git functions should probably all use parseargs, like git push
    #TODO: These git functions all follow the same pattern.
    #               Refactor these so they only contain their unique logic
    #TODO: Add jsbain's keychain addition. Need to figure out how to
    #               Add ipad-specific modules without breaking Shellista everywhere
    #TODO: If there is no ~/.gitconfig file, set up the username and passworde

    #Find a git repo dir
    def _find_repo(path):
        subdirs = os.walk(path).next()[1]
        if '.git' in subdirs:
            return path
        else:
            parent = os.path.dirname(path)
            if parent == path:
                return None
            else:
                return _find_repo(parent)


    #Get the parent git repo, if there is one
    def _get_repo():
        return Gittle(_find_repo(os.getcwd()))


    def git_init(args):
        if len(args) == 1:
            Gittle.init(args[0])
        else:
            print command_help['init']

    def git_status(args):
        if len(args) == 0:
            repo = _get_repo()
            status = porcelain.status(repo.repo)
            print status
        else:
            print command_help['git_staged']

    def git_remote(args):
        '''List remote repos'''
        if len(args) == 0:
            repo = _get_repo()
            for key, value in repo.remotes.items():
                print key, value
        else:
            print command_help['remote']

    def git_add(args):
        if len(args) > 0:
            repo = _get_repo()
            args = [os.path.join(os.path.relpath('.', repo.path),x) for x in args]
            #repo.stage(args)
            porcelain.add(repo.repo, args)
        else:
            print command_help['add']

    def git_rm(args):
        if len(args) > 0:
            repo = _get_repo()
            args = [os.path.join(os.path.relpath('.', repo.path),x) for x in args]
            #repo.rm(args)
            porcelain.rm(repo.repo, args)
        else:
            print command_help['rm']

    def git_branch(args):
        if len(args) == 0:
            repo = _get_repo()
            active = repo.active_branch
            for key, value in repo.branches.items():
                print ('* ' if key == active else '') + key, value
        else:
            print command_help['branch']

    def git_reset(args):
        if len(args) == 0:
            repo = _get_repo()
            porcelain.reset(repo.repo, 'hard')
        else:
            print command_help['reset']

    def git_commit(args):
        if len(args) == 3:
            try:
                repo = _get_repo()
                #print repo.commit(name=args[1],email=args[2],message=args[0])
                author = "{0} <{1}>".format(args[1], args[2])
                print porcelain.commit(repo.repo, args[0], author, author )
            except:
                print 'Error: {0}'.format(sys.exc_value)
        else:
            print command_help['commit']

    def git_clone(args):
        if len(args) > 0:
            url = args[0]

            repo = Gittle.clone(args[0], args[1] if len(args)>1 else '.', bare=False)

            #Set the origin
            config = repo.repo.get_config()
            config.set(('remote','origin'),'url',url)
            config.write_to_path()
        else:
            print command_help['clone']

    def git_pull(args):
        if len(args) <= 1:
            repo = _get_repo()
            url = args[0] if len(args)==1 else repo.remotes.get('origin','')
            if url:
                repo.pull(origin_uri=url)
            else:
                print 'No pull URL.'
        else:
            print command_help['git pull']



    def git_push(args):
        parser = argparse.ArgumentParser(prog='git push'
                                         , usage='git push [http(s)://<remote repo>] [-u username[:password]]'
                                         , description="Push to a remote repository")
        parser.add_argument('url', type=str, nargs='?', help='URL to push to')
        parser.add_argument('-u', metavar='username[:password]', type=str, required=False, help='username[:password]')
        result = parser.parse_args(args)

        user, sep, pw = result.u.partition(':') if result.u else (None,None,None)

        repo = _get_repo()
        
        #Try to get the remote origin
        if not result.url:
            result.url = repo.remotes.get('origin','')

        branch_name = os.path.join('refs','heads', repo.active_branch)  #'refs/heads/%s' % repo.active_branch

        print "Attempting to push to: {0}, branch: {1}".format(result.url, branch_name)

        netloc = urlparse.urlparse(result.url).netloc

        keychainservice = 'shellista.git.{0}'.format(netloc)

        if sep and not user:
            # -u : clears keychain for this server
            for service in keychain.get_services():
                if service[0]==keychainservice:
                    keychain.delete_password(*service)

        #Attempt to retrieve user
        if not user and SAVE_PASSWORDS:
            try:
                user = dict(keychain.get_services())[keychainservice]
            except KeyError:
                user, pw = console.login_alert('Enter credentials for {0}'.format(netloc))

        if user:
            if not pw and SAVE_PASSWORDS:
                pw = keychain.get_password(keychainservice, user)

            #Check again, did we retrieve a password?
            if not pw:
                user, pw = console.login_alert('Enter credentials for {0}'.format(netloc), login=user)
                #pw = getpass.getpass('Enter password for {0}: '.format(user))

            opener = auth_urllib2_opener(None, result.url, user, pw)

            print porcelain.push(repo.repo, result.url, branch_name, opener=opener)
            keychain.set_password(keychainservice, user, pw)

        else:
            print porcelain.push(repo.repo, result.url, branch_name)

    def git_modified(args):
        repo = _get_repo()
        for mod_file in repo.modified_files:
            print mod_file

    def git_log(args):
        if len(args) <= 1:
            try:
                repo = _get_repo()
                porcelain.log(repo.repo, max_entries=int(args[0]) if len(args)==1 else None)
            except ValueError:
                print command_help['log']
        else:
            print command_help['log']


    def git_checkout(args):
        if len(args) in [1,2]:
            repo = _get_repo()
            if len(args) == 1:
                repo.clean_working()
                repo.switch_branch('{0}'.format(args[0]))

            #Temporary hack to get create branch into source
            #TODO: git functions should probably all user parseargs, like git push
            if len(args) == 2:
                if args[0] == '-b':
                    #TODO: Add tracking as a parameter
                    print "Creating branch {0}".format(args[1])
                    repo.create_branch(repo.active_branch, args[1], tracking=None)
                    #Recursive call to checkout the branch we just created
                    git_checkout([args[1]])
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
    ,'reset': git_reset
    ,'status': git_status
    ,'help': git_help
    }

    command_help = {
    'init':  'git init <directory> - initialize a new Git repository'
    ,'add': 'git add <file1> .. [file2] .. - stage one or more files'
    ,'rm': 'git rm <file1> .. [file2] .. - unstage one or more files'
    ,'commit': 'git commit <message> <name> <email> - commit staged files'
    ,'clone': 'git clone <url> [path] - clone a remote repository'
    ,'modified': 'git modified - show what files have been modified'
    ,'log': 'git log [number of changes to show] - show a full log of changes'
    ,'push': 'git push [http(s)://<remote repo>] [-u username[:password]] - push changes back to remote'
    ,'pull': 'git pull [http(s)://<remote repo>] - pull changes from a remote repository'
    ,'checkout': 'git checkout <branch> - check out a particular branch in the Git tree'
    ,'branch': 'git branch - show branches'
    ,'status': 'git status - show status of files (staged, unstaged, untracked)'
    ,'reset': 'git reset - reset a repo to its pre-change state'
    ,'help': 'git help'
    }

    #git_init.__repr__ = "git init abc"

    args = bash(line)

    try:
        #Call the command and pass args
        cmd = commands.get(args[0] if len(args) > 0 else 'help','help')
        cmd(args[1:])
    except:
        #import traceback
        #traceback.print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)
        #traceback.print_tb(sys.exc_traceback)
        print 'Error: {0}'.format(sys.exc_value)

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



