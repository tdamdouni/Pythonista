# Introduction
StaSH comes with a few tools for working with git repos.  This tutorial will cover a few basic workflows for deal with git repositories in atash/Pythonista specifically.  It helps to be familiar with git commandline tools, although the git in stash is missing a great many features that you might be used to.

## Creating a repo from scratch
You have a new idea for a project.  Maybe you have some cool code you'd like to share.  Fire up stash, and let's begin.

There are a few basic options when creating new work.  First is to create a local git repo, and work locally.  When you are ready to publish, you would create a bare github repo, then push to it.  Second is to create the github repo first, clone it back locally, and then start adding files.  The first method takes a few extra steps, but is more appropriate when you already have files created.

Let's start by creating the github repo, using the `gh create` command.  First let's review the help:

```bash
[~/Documents]$ gh create --help
Usage: gh create [options] <name> 

	Options:
	-h, --help             This message
	-s <desc>, --description <desc>		Repo description
	-h <url>, --homepage <url>				Homepage url
	-p, --private          private
	-i, --has_issues       has issues
	-w, --has_wiki  			 has wiki
	-d, --has_downloads    has downloads
	-a, --auto_init     		create readme and first commit
	-g <ign>, --gitignore_template <ign>  create gitignore using string
``` 

To create a bare repo, use `gh create <name>`, otherwise for auto init, use `gh create -a <name>`.  Let's create a basic repo with downloads, issue tracker, and autoinit.

```bash
[~/Documents]$ gh create -aid -s "stash git tools tutorial" stash_git_tutorial
Created https://github.com/jsbain/stash_git_tutorial
``` 

Now, magically, a github repo named stash_git_tutorial has been created.  Since we used auto init, the repo has a Readme.md file created, and the first commit.

Let's pull this locally so we can start working.

## Cloning a repo
We have a repo, let's clone it.  A few gotchas to watch out for: the url should be of the form either an ssh:/git@github.com/owner/repo.git, or https://github.com/owner/repo.git.  A later chapter will discuss how to setup ssh (I totally reccommend it, since the http implementation in dulwich seems to not always play well with github.). Don't forget the .git extension!
Also, don't forget the second argument to clone, which is the folder to clone to.  Leaving it blank will try to clone to the current folder, which is fine if you have alreeady created and cd'd to a folder, but only causes problems if run from ~/Documents.

```bash 
[~/Documents]$ git clone https://github.com/jsbain/stash_git_tutorial.git git_tutorial
[~/Documents]$ cd git_tutorial/
[git_tutorial]$ ll
.git (374.0B) 2016-02-25 00:47:43
README.md (46.0B) 2016-02-25 00:47:43
``` 

So now we have a copy of the repo on our local device.  The .git folder is special, do not delete it.  A future installment will talk a little about what is in here, since it can sometimes be useful to know a little about the plumbing for times when things go horribly wrong (as long as you don't delete this folder, even if you make a terible mistake, your committed files are safe and can be recovered.  dulwich never really does garbage collection, so objects in the repo will always be there. )

## Adding some files, and our first commit
Let's go ahead and create some files.  I will go ahead and save this file to that folder.

``` 
git_tutorial]$ ll
.git (374.0B) 2016-02-25 00:47:43
README.md (46.0B) 2016-02-25 00:47:43
stash_git_tutorial.md (3.5K) 2016-02-25 01:00:58
[git_tutorial
``` 
The `git add` command is used to add a file to the "index".  There are some good docs describing how git works, but the basic idea is this:  you have a working copy of a folder structure -- basically the files that you see and can edit.  Internal to git, there is another "folder" called the index, or staging area, where you can copy files to create a commit.  The index is a temporary staging area, starts off containing whatever was in the last commit.    When you commit, you create a permanent snapshot of what is in the index at that time.   This act of copying to the staging area in git parlance is called `git add`, and `git commit` creates the snapshot which is then permanently stored.   `git status` checks the index to see if it is up to date with the working copy.  Let us add, then commit, and check status to verify we have added the file.

```bash
[git_tutorial]$ git add stash_git_tutorial.md 
Adding stash_git_tutorial.md

# let's check that the file was added
[git_tutorial]$ git status
STAGED
add['stash_git_tutorial.md']
UNSTAGED LOCAL MODS
[]

#commit the file
[git_tutorial]$ git commit
Commit Message: Initial commit of tutorial
Author Name: JonB
Save this setting? [y/n]y
Author Email: jsbain@[.....]
Save this setting? [y/n]y
e2a369919bc887bb79690420b5765d0ac525dd4d
``` 

The first time you commit to a repo in stash, it will prompt you to save author name and email so future commits need only the message.  The commit message describes in a few words what the purpose of the commit is.  The 20 digits spit out after committing is called the sha, which is basicslly a hash of everything in the staging area and the current time, author, and commit message info.  
Usually this gets truncated to 6-7 digits.

Let's add a few more files to the folder, then add them to the repo.


```bash 
[git_tutorial]$ echo 'sample file A' > samplea.txt
[git_tutorial]$ echo 'sample file B' > sampleb.txt


[git_tutorial]$ git status
STAGED
UNSTAGED LOCAL MODS
['stash_git_tutorial.md']

[git_tutorial]$ git add *
Adding README.md
Adding samplea.txt
Adding sampleb.txt
Adding stash_git_tutorial.md

[git_tutorial]$ git status
STAGED
add['sampleb.txt', 'samplea.txt']
modify['stash_git_tutorial.md']
UNSTAGED LOCAL MODS
[]
``` 

Note that since I have been continuing to update this file as I write, the first git status shows me that I have uncommitted changes -- these are not stored anywhere yet, other than your working copy.  I used git add with wildcards.  After, status shows the new files, as well as the fact that this file is modified in the staging area, compared to the last commit.

Sometimes it is useful to use `git diff` to remind yourself of the changes you have made.  The gitview program has a visual diff display which is somewhat easier to look at.

``` 
[git_tutorial]$ git diff
diff --git /dev/null b/samplea.txt
new mode 100644
index 0000000..e8d2873 100644
--- /dev/null
+++ b/samplea.txt
@@ -1,0 +1,1 @@
+sample file A
diff --git /dev/null b/sampleb.txt
new mode 100644
index 0000000..80ad0f9 100644
--- /dev/null
+++ b/sampleb.txt
@@ -1,0 +1,1 @@
+sample file B
diff --git a/stash_git_tutorial.md b/stash_git_tutorial.md
index fc18f02..b982ec5 100644
--- a/stash_git_tutorial.md
+++ b/stash_git_tutorial.md
@@ -58,8 +58,28 @@
+The `git add` command is used to add a file to the "index" 
[...]
``` 

``` 
[git_tutorial]$ git status
STAGED
add['sampleb.txt', 'samplea.txt']
modify['stash_git_tutorial.md']
UNSTAGED LOCAL MODS
[]
[git_tutorial]$ git commit "Added some files and caught up with tutorial"
8509bbf0116a29076099e3db5c0ba3e57b1d43d9
``` 

# Pushing back to github
Finally, we want the world to see the great progress we are making.  Time to push back to github.  If you have cloned using the git clone module, git push will push the changes to origin. A later chapter will discuss remotes, how to add or change.

``` 
[git_tutorial]$ git push
Attempting to push to: https://github.com/jsbain/stash_git_tutorial.git, branch: refs/heads/master
Push to https://jsbain:********@github.com/jsbain/stash_git_tutorial.git successful.
success!
``` 


#TODO
Future topics:
1) creating bare repos and pushing to gh
2) forking someone elses' repo
3) pull requests
4) branches
5) pulling, fetching and merging
6) multiple remote workflows
7) what to do when things go horribly wrong
8) reverting changes (git reset)
