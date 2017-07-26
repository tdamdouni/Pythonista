Github-Cheatsheet
=================

_https://github.com/humberry/Github-Cheatsheet_

#### Howto create a new public remote repo via StaSh v0.6.1 or CreateRepo.py  

First you need a Personal access token.  
Github login > Settings > Personal access tokens > Generate new token > Token description: OnlyPublicRepo > only check public_repo > Generate token > copy the displayed token to the clipboard  
  
curl -X 'POST' -H 'Authorization: token TokenFromClipboard' -d '{"name": "RepoNameToBeInsert", "auto_init": true, "private": false}' https://api.github.com/user/repos  
  
or use CreateRepo.py
  
  
#### Howto download your own repo, change a file and push it via StaSh v0.6.1  

[~/Documents]$ **mkdir Github**  
[~/Documents]$ **cd Github**  
[Github]$ **mkdir ui-tutorial**  
[Github]$ **cd ui-tutorial** 
  
[ui-tutorial]$ **git clone https://github.com/humberry/ui-tutorial.git** 
  
[ui-tutorial]$ **ll**  
.git (374.0B) 2016-02-16 21:27:36  
...  
MiniPhotoView.py (3.4K) 2016-02-16 21:28:55  
...  
  
[ui-tutorial]$ **edit MiniPhotoView.py**  
[ui-tutorial]$ **git status**  
STAGED  
UNSTAGED LOCAL MODS  
['MiniPhotoView.py']  
  
[ui-tutorial]$ **git add MiniPhotoView.py**  
Adding MiniPhotoView.py  
  
[ui-tutorial]$ **git commit**  
Commit Message: remove touch and layout method  
Author Name: humberry  
Save this setting? [y/n]y  
Author Email:   
Save this setting? [y/n]y  
shivrztvhf...  
  
[ui-tutorial]$ **git push**  
Attempting to push to: https://github.com/humberry/ui-tutorial.git, branch: refs/heads/master  
Enter username: humberry  
Enter password: mysecretpassword  
Push to https://humberry:mysecretpassword@github.com/humberry/ui-tutorial.git successful.  
success!
