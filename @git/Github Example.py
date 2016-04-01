# coding: utf-8

# https://gist.github.com/mmurdoch/4051357

import console
import keychain
import traceback
from github import Github

def printRepository(username):
	g = Github(username, getGithubPassword(username))

	user = g.get_user()
	repositories = user.get_repos()

	for repository in repositories:
		print repository.name
		printBranches(repository)

def printBranches(repository):
	for branch in repository.get_branches():
		print '  ', branch.name
		tree = branch.commit.commit.tree
		printTree(repository, tree, '    ')

def printTree(repository, tree, indent):
	for element in tree.tree:
		print indent, element.path
		if element.type == 'tree':
			printTree(repository, repository.get_git_tree(element.sha), indent + '  ')

def getGithubPassword(username):
	service = 'github'
	password = keychain.get_password(service, username)
	if password == None:
		print "Enter password for user", username
		password = console.secure_input()
		keychain.set_password(service, username, password)
	return password

# Pass your Github username as a parameter
printRepository('tdamdouni')