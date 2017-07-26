#!/usr/bin/env python3
# coding: utf-8

# Workflow: * In _Working Copy_ open a GitHub repository that you want copied into _Pythonista_ * if your needs are more modest, you can even select a single file or folder * Click the Share icon at the upper right corner of the Working Copy screen * Click Run Pythonista Script * Click on this script * Click the run button

# When you [return to Pythonista](pythonista://) your files should be in the 'from Working Copy' directory.

## Pythonista --> Working Copy: Working Copy has a "__save to Working Copy__" Share Sheet action (you might have to enable in Share Sheet, More...)

# Workflow A -- a single file: * Open the file of interest in the Pythonista editor * Click the wrench icon at the upper right * Click the "Share..." button * Click "Save in Working Copy" button * Select the repo that you want to save the file into * Click "Save As..." * Change the filename if you want to and click "Save As..." again * Click "Just Save" if you want to bundle multiple files into a single commit --or-- Type your commit message and click "Commit"

# Workflow B -- a folder or a file: * Click `Edit` in the Pythonista file browser * Select the folder or file of interest * Click the Share icon at the bottom of the file browser * Click "Save in Working Copy" button * Select "Import as Repository" or "Save as Directory"

# Note: When selecting multiple folders or multiple files, only the first one is processed.

# __Now we have an end to end workflow: GitHub --> Working Copy --> Pythonista --> Working Copy --> GitHub__

# See: https://forum.omz-software.com/topic/2382/git-or-gist-workflow-for-pythonista/24

# Appex script to copy a git file, folder, or repo from the Working Copy app

import appex, os, shutil

from_wc = os.path.abspath(os.path.expanduser('from Working Copy'))


def main():
	if appex.is_running_extension():
		file_paths = appex.get_file_paths()
		assert len(file_paths) == 1, 'Invalid file paths: {}'.format(file_paths)
		srce_path = file_paths[0]
		dest_path = srce_path.split('/File Provider Storage/')[-1]
		dest_path = os.path.join(from_wc, dest_path)
		file_path, file_name = os.path.split(dest_path)
		if not os.path.exists(file_path):
			os.makedirs(file_path)
		if os.path.isdir(srce_path):
			shutil.rmtree(dest_path, ignore_errors=True)
			print(shutil.copytree(srce_path, dest_path))
		else:
			print(shutil.copy2(srce_path, dest_path))
		print('{} was copied to {}'.format(file_name, file_path))
	else:
		print('''* In Working Copy app select a repo, file, or directory to be
		copied into Pythonista.  Click the Share icon at the upperight.  Click Run
		Pythonista Script.  Pick this script and click the run button.  When you return
		to Pythonista the files should be in the 'from Working Copy'
		directory.'''.replace('\n', ' ').replace('.  ', '.\n* '))
		
if __name__ == '__main__':
	main()

