gitview
=======

Pythonista git wrapper
-----------------------
This is a basic git front end, built upon gittle and dulwich.  The basic idea is to make git on the ipad an easier proposition.  some of the key features:
    * Select repo from a dropdown list, which crawls the entire Script a library, or manually type a path.  also, if gitui id run fro  the action menu, the repo contsining the open file will be loaded.
    * To create a new repo, either press the new repo button, to start a blank repo, or press clone button and specify a git address, (e.g. https://github.com/jsbain/gitview.git) along with the hlocation to clone.
    * once a repo is selected, the branch dropdown allows selection or direct entry of a branch.  selecting a branch only loads the index, it does not change any files:  use checkout to overwrite the current working directory with the contents of the committed tree. To perform a crude form of merge/rebase, checkout branch with the changes, then select ( but do not checkout) the branch to merge to, stage the changes, and commit.  
    * add a new branch by simply typing in a new name (delete not yet supported)
    * push and pull to a remote are supported; type remote url in the remote dropdown.  this will create a shortcut for origin (other remotes are supported, if manually editing config.)
    * the files in the repo, categorized by their change state, are shown in the lower section.  pull doen and release to refresh this table, if edits have been made elsewhere.   various actions are avilable depending on the state:
        ➕ add/stage a modification or new file
        ✖️remove (stage for removal) a file from tracking
        [undo] unstage change
        ↹ show diff
        [doc] open a file
    * push and pull from remote repos works... but be careful.  push only works if an identically named branch exists on the remote.
    pull might override an existing branch, though thoe object is still there somewhere im the object store...  there is 
    matching named branches get overwritten.
    * push will reuse credentials from shellista, if youve used git in shellista before.

         
install
=======
use GitHubGet or other tool to download repo.
first run install_gitview once to load dulwich,etc to site-packages
run gitui to run
                                                                                                                    
todo
====
handle remote branches better in pull
three way merge. merge_head, etc
log browser improvements
restructure code
sidebar or menubar when editing code, allowing quick commit!


                                                                                                        
