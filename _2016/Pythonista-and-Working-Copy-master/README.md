# Pythonista and Working Copy

![alt text](https://img.shields.io/badge/Python-2.7-blue.svg "Python 2.7")
![alt text](https://img.shields.io/badge/Python-3.5-blue.svg "Python 3.5")

## Working Copy --> Pythonista
### Note: Working Copy has recently made changes that might make much of this unnecessary!
### Please try to share a file or repo from Working Copy to Pythonista (or Editorial) and you will get an "Install a Workflow" message...

[Appex script](http://omz-software.com/pythonista/docs/ios/appex.html) that enables Pythonista to download a git repo, file, or folder from a share sheet from the Working Copy app

Pre requisites:
* [Pythonista for iOS](http://omz-software.com/pythonista/)
* [Working Copy app for iOS](https://workingcopyapp.com)

Workflow:
* In _Working Copy_ open a GitHub repository that you want copied into _Pythonista_
  * if your needs are more modest, you can even select a single file or folder
* Click the Share icon at the upper right corner of the Working Copy screen
* Click Run Pythonista Script
* Click on this script
* Click the run button

When you [return to Pythonista](pythonista://) your files should be in the 'from Working Copy' directory.

## Pythonista --> Working Copy
Working Copy has a "__save to Working Copy__" Share Sheet action (you might have to enable in Share Sheet, More...)

Workflow A -- a single file:
* Open the file of interest in the Pythonista editor
* Click the wrench icon at the upper right
* Click the "Share..." button
* Click "Save in Working Copy" button
* Select the repo that you want to save the file into
* Click "Save As..."
* Change the filename if you want to and click "Save As..." again
* Click "Just Save" if you want to bundle multiple files into a single commit --or-- Type your commit message and click "Commit"

Workflow B -- a folder or a file:
* Click `Edit` in the Pythonista file browser
* Select the folder or file of interest
* Click the Share icon at the bottom of the file browser
* Click "Save in Working Copy" button
* Select "Import as Repository" or "Save as Directory"

Note: When selecting multiple folders or multiple files, only the first one is processed.

__Now we have an end to end workflow: GitHub --> Working Copy --> Pythonista --> Working Copy --> GitHub__

See: https://forum.omz-software.com/topic/2382/git-or-gist-workflow-for-pythonista/24
