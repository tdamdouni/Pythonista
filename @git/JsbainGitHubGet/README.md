GitHubGet
=========

Quick script to zip and download a repo from github, for those afraid of shellista


Two ways to use:
1) copy url into clipboard, and run
2). Use bookmarklet
javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://GitHubGet?action=run&argv='+document.location.href;%7D)();

In either case, just go to main github repo page, and/or choose the branch you want cloned.  Script should be able to figure out user, repo, and branch, downloads the zip of the repo to a temp file, unzips into main script folder (will be under folder named repo-branch, for instance GitHubGet-master/ for this repo).

This script makes no attempt to check if you've downloaded a repo before, nor does it distinguish the folder based on username.  
