# Note that this script attempts to delete directories (Folders) called 'temp' and 'dateutil'
# within Pythonista as part of installation. It will also overwrite files in directories 
# named 'github' and 'githubista'. If you are using Pythonista 1.3 or above please check
# that you have not created any Folders with these names before running this script as
# any files inside them will be irretrievably lost.
import os
import urllib2
import tarfile
import shutil
import traceback

# Downloads and installs the dateutil library into a directory called 'dateutil' 
# alongside your saved Pythonista scripts.
# It also creates a directory called 'temp' during the installation process which 
# is deleted after installation.
def getDateutil():
	workingPath = os.getcwd()
	tempPath = os.path.join(workingPath, 'temp')
	dateutilArchiveDir = 'python-dateutil-1.5'
	dateutilArchive = dateutilArchiveDir + '.tar.gz'
	dateutilArchivePath = os.path.join(tempPath, dateutilArchive)

	try:
		os.mkdir(tempPath)
	except OSError:
		pass

	print 'Downloading dateutil archive'
	dateutilArchiveUrl = urllib2.urlopen('http://labix.org/download/python-dateutil/' + dateutilArchive)
	localArchive = open(dateutilArchivePath, 'w')
	localArchive.write(dateutilArchiveUrl.read())
	localArchive.close()
	dateutilArchiveUrl.close()
	archive = tarfile.open(dateutilArchivePath, 'r:gz')

	print 'Extracting dateutil library from archive'
	try:
		os.chdir(tempPath)
		archive.extractall()
	finally:
		archive.close()
		os.chdir(workingPath)

	dateutilDir = 'dateutil'
	tempDateutilPath = os.path.join(os.path.join(tempPath, dateutilArchiveDir), dateutilDir)
	dateutilPath = os.path.join(workingPath, dateutilDir)

	print 'Installing dateutil'
	shutil.rmtree(dateutilPath, True)
	shutil.copytree(tempDateutilPath, dateutilPath)
	shutil.rmtree(tempPath)
	
	print 'dateutil installed'

# Downloads and installs the PyGithub library into a directory called 'github' 
# alongside your saved Pythonista scripts.
# This directory is not visible in Pythonista (as of version 1.2) and should not 
# conflict with a script of the same name
# as Pythonista automatically appends '.py' to all scripts before saving them.
def getPyGithub():
	# Use this to install a version of PyGithub which uses dateutil 
	# rather than strptime
	githubUser = 'mmurdoch'
	# Use this to install the original version of PyGithub.
	# This uses strptime rather than dateutil but strptime throws an error the 
	# second time it's called...
	#githubUser = 'jacquev6' # Original PyGithub author
	pythonistaDir = os.getcwd()
	githubDir = os.path.join(pythonistaDir, 'github')

	try:
		os.mkdir(githubDir)
	except OSError:
		pass

	# All the files. It would be better to fetch this list from github to ensure 
	# that any changes to this list in future are automatically picked up.
	pyGithubFiles = ['AuthenticatedUser.py', 'Authorization.py', 'AuthorizationApplication.py',
                     'Branch.py', 'Commit.py', 'CommitComment.py', 'CommitStats.py',
                     'CommitStatus.py', 'Comparison.py', 'ContentFile.py', 'Download.py',
                     'Event.py', 'File.py', 'Gist.py', 'GistComment.py', 'GistFile.py',
                     'GistHistoryState.py', 'GitAuthor.py', 'GitBlob.py', 'GitCommit.py',
                     'GitObject.py', 'GitRef.py', 'GitTag.py', 'GitTree.py', 'GitTreeElement.py',
                     'GithubException.py', 'GithubObject.py', 'GitignoreTemplate.py', 'Hook.py',
                     'HookDescription.py', 'HookResponse.py', 'InputFileContent.py', 'InputGitAuthor.py',
                     'InputGitTreeElement.py', 'Issue.py', 'IssueComment.py', 'IssueEvent.py',
                     'IssuePullRequest.py', 'Label.py', 'Legacy.py', 'MainClass.py', 'Milestone.py',
                     'NamedUser.py', 'Notification.py', 'NotificationSubject.py', 'Organization.py',
                     'PaginatedList.py', 'Permissions.py', 'Plan.py', 'PullRequest.py',
                     'PullRequestComment.py', 'PullRequestMergeStatus.py', 'PullRequestPart.py',
                     'Repository.py', 'RepositoryKey.py', 'Requester.py', 'Tag.py',
                     'Team.py', 'UserKey.py', '__init__.py']

	print 'Downloading and installing PyGithub'
	
	for file in pyGithubFiles:
		print 'Downloading', file
		localFile = open(os.path.join(githubDir, file), 'w')
		resource = urllib2.urlopen('https://raw.github.com/' + githubUser + '/PyGithub/master/github/' + file)
		localFile.write(resource.read())
		localFile.close()
		resource.close()
	
	print 'PyGithub downloaded and installed'

# Downloads and installs the githubista library into a directory called 'githubista' 
# alongside your saved Pythonista scripts.
# This directory is not visible in Pythonista (as of version 1.2) and should not 
# conflict with a script of the same name as Pythonista automatically appends '.py' 
# to all scripts before saving them.
def getGithubista():
	githubUser = 'mmurdoch'
	pythonistaDir = os.getcwd()
	githubDir = os.path.join(pythonistaDir, 'githubista')

	try:
		os.mkdir(githubDir)
	except OSError:
		pass

	# All the files. It would be better to fetch this list from github to ensure that any changes
	# to this list in future are automatically picked up.
	files = ['githubista.py', 'github_clone.py', 'github_commit.py', '__init__.py']

	print 'Downloading and installing githubista'
	
	for file in files:
		print 'Downloading', file
		localFile = open(os.path.join(githubDir, file), 'w')
		resource = urllib2.urlopen('https://raw.github.com/' + githubUser + '/githubista/master/' + file)
		localFile.write(resource.read())
		localFile.close()
		resource.close()
	
	print 'githubista downloaded and installed'	

try:
	getDateutil()
	getPyGithub()
	getGithubista()
	
except:
	traceback.print_exc()