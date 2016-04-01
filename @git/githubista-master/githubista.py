import base64
import console
import editor
from github import *
import keychain
import os
import traceback

def login():
	username, password = load_credentials()

	try:
		username, password = console.login_alert('Github Login', '', username, password, 'Login')
	except KeyboardInterrupt:
		return None

	save_credentials(username, password)

	return Github(username, password).get_user()

def get_current_repository_name():
	repository_dir = get_current_repository_dir()
	if repository_dir is None:
		return None
		
	return os.path.split(repository_dir)[1]

def get_current_repository(user):
	repository_name = get_current_repository_name()
	return user.get_repo(repository_name)

def clone():
	try:
		user = login()
		if user != None:
			try:
				repository_name = console.input_alert('Repository Name', '', '', 'Clone')
				clone_authenticated(user, repository_name)
			except KeyboardInterrupt:
				return
	except:
		traceback.print_exc()	

def clone_authenticated(user, repository_name, branch_name = 'master'):
	pythonista_dir = os.getcwd()
	repository_dir = create_directory_if_missing(pythonista_dir, repository_name)
	git_dir = create_directory_if_missing(repository_dir, '.git')

	head_file = os.path.join(git_dir, 'HEAD')
	head_ref = 'ref: ' + get_branch_head_ref_name(branch_name)

	with open(head_file, 'w') as head_file_descriptor:
		head_file_descriptor.write(head_ref)

	repository = user.get_repo(repository_name)
	branch_head_commit = get_branch_head_commit(user, repository, branch_name)
	clone_commit(repository, repository_dir, branch_head_commit)

def commit():
	try:
		user = login()
		if user != None:
			try:
				commit_message = console.input_alert('Commit Message', '', '', 'Commit')
				commit_authenticated(user, commit_message)
			except KeyboardInterrupt:
				return
	except:
		traceback.print_exc()

def commit_authenticated(user, commit_message):
	path = editor.get_path()
	tree_path, blob_name = os.path.split(path)

	repository = get_current_repository(user)

	blob = repository.create_git_blob(editor.get_text(), 'utf-8')

	parent_commit = get_current_head_commit(user)
	
	original_tree = repository.get_git_tree(parent_commit.tree.sha, True)

	tree_elements = []
	for original_element in original_tree.tree:
		element_sha = original_element.sha
		if blob_name == original_element.path:
			element_sha = blob.sha

		element = InputGitTreeElement(
			original_element.path,
			original_element.mode,
			original_element.type,
			sha = element_sha)
		tree_elements.append(element)

	tree = repository.create_git_tree(tree_elements)
	# Need to update all ancestor trees as well
	
	commit = repository.create_git_commit(commit_message, tree, [parent_commit])

	current_branch_head_ref = 'heads/' + get_current_branch_name()
	head_ref = repository.get_git_ref(current_branch_head_ref)
	head_ref.edit(commit.sha)

def get_current_head_commit(user):
	repository_name = get_current_repository_name()
	branch_name = get_current_branch_name()
	repository = user.get_repo(repository_name)
	return get_branch_head_commit(user, repository, branch_name)

def get_current_repository_dir():
	git_dir = get_current_git_dir()
	if git_dir == None:
		return None
	
	return get_parent_dir(git_dir)

def get_current_git_dir():
	previous_dir = ''
	current_dir = editor.get_path()
	git_dir_name = '.git'
	git_dir = os.path.join(current_dir, git_dir_name)
	while not os.path.isdir(git_dir):
		previous_dir = current_dir
		current_dir = get_parent_dir(current_dir)
		if current_dir == previous_dir:
			return None
		git_dir = os.path.join(current_dir, git_dir_name)
		
	return git_dir

def get_parent_dir(child_dir):
	return os.path.split(child_dir)[0]

def get_current_branch_name():
	git_dir = get_current_git_dir()
	if git_dir == None:
		return None

	head_file = os.path.join(git_dir, 'HEAD')
	head_ref = read_ref(head_file)

	return head_ref.split('/').pop()

def read_ref(ref_file):
	ref = ''
	with open(ref_file, 'r') as ref_file_descriptor:
		ref = ref_file_descriptor.read()

	return ref

def get_branch_head_commit(user, repository, branch_name):
	branch_head_ref = get_branch_head_ref(repository, branch_name)
	return repository.get_git_commit(branch_head_ref.object.sha)

def get_branch_head_ref_name(branch_name):
	return 'refs/heads/' + branch_name

def get_branch_head_ref(repository, branch_name):
	branch_head_ref = None

	for ref in repository.get_git_refs():
		if ref.ref.startswith(get_branch_head_ref_name(branch_name)):
			branch_head_ref = ref

	return branch_head_ref

def create_directory_if_missing(parent_absolute_dir_name, dir_name):
	absolute_dir_name = os.path.join(parent_absolute_dir_name, dir_name)
	try:
		os.mkdir(absolute_dir_name)
	except OSError:
		pass
		
	return absolute_dir_name

def clone_commit(repository, repository_dir, commit):
	head_tree = commit.tree
	tree = repository.get_git_tree(head_tree.sha, True)
	save_recursive_tree(repository, repository_dir, tree.tree)

def save_recursive_tree(repository, repository_dir, tree):
	for element in tree:
		save_element(repository, repository_dir, element)

def save_element(repository, repository_dir, element):
	if element.type == 'blob':
		blob = repository.get_git_blob(element.sha)
		content = ''
		if blob.encoding == 'base64':
			content = base64.b64decode(blob.content)
		else:
			raise Exception('Unknown encoding: ' + blob.encoding)

		blob_file = os.path.join(repository_dir, element.path)
		with open(blob_file, 'w') as blob_file_descriptor:
			blob_file_descriptor.write(content)
	elif element.type == 'tree':
		create_directory_if_missing(repository_dir, element.path)

def get_username_service():
	return 'github_username'

def get_password_service():
	return 'github_password'

def load_credentials():
	username = keychain.get_password(get_username_service(), 'username')
	password = None
	if username is not None:
		password = keychain.get_password(get_password_service(), username)
		
	if username is None:
		username = ''
		
	if password is None:
		password = ''

	return username, password
	
def save_credentials(username, password):
	keychain.set_password(get_username_service(), 'username', username)
	keychain.set_password(get_password_service(), username, password)