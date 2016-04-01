#githubista

Access your Github account from the [Pythonista iPad app](https://itunes.apple.com/gb/app/pythonista/id528579881?mt=8).

##Installation
1. The installation script attempts to delete directories (Folders) called 'temp' and 'dateutil' 
within Pythonista as part of installation. It will also overwrite files in directories named
'github' and 'githubista'. If you are using Pythonista 1.3 or above **please check that you
have not created any Folders with these names before running this script as any files inside
them will be irretrievably lost**!
2. Run the following script: https://gist.github.com/4026453

The installation creates 'github' and 'dateutil' directories in Pythonista's Documents
directory which you can import as modules. It also creates a 'githubista' directory
in which you'll find a couple of using scripts for cloning a repository and committing
changes.

From version 1.3 onwards of Pythonista these directories are visible through the UI.
If you are using version 1.2 or below then you can see them, for example, by running
@wrenoud's fantastic file browser (see http://omz-software.com/pythonista/forums/discussion/19).

The 'github' directory contains a patched version of [PyGithub](https://github.com/mmurdoch/PyGithub).
PyGithub provides a full implementation of the Github v3 API. For browsing operations the API
is fairly self explanatory but for committing changes it is somewhat obfuscated
(http://developer.github.com/v3/git/ is the best resource for help with understanding this).
In principle, though, a fully featured Github client could be built on top of this implementation.

PyGithub has been patched to to use dateutil rather than strptime as it gives errors the second
time `strptime` is called (a quick google suggests that this is a fairly common problem). It's
this patched version which is downloaded and installed, although you can try the original by
reading the comments embedded in the script if you'd like. This is also the reason that dateutil
is installed - the original PyGithub library has no dependency on it.

An example use of the PyGithub module (which authenticates a Github user and lists the
files in their public and private repositories) can be found here: https://gist.github.com/4051357

## Included Functionality
### Cloning a Repository
Once installed, to clone a github repository, simply run the following script. It will prompt for
your github credentials and the name of the repository you want to clone.

    import githubista

    githubista.clone()

The repository is cloned to a directory with the same name. To access the files within you will need
to use Pythonista 1.3 or above or a file browser tool such as the one linked to above.

### Committing Changes
Once you've made changes to a script file you can commit the changes by running the following script
from the actions menu:

    import githubista

    githubista.commit()

This script will ask for credentials again (although it remembers the previously entered ones) and
also asks for the commit message.

### Limitations
1. Only the master branch is cloned - you cannot currently choose a different branch
2. Only a single file can be committed at a time
3. Only a flat structure is supported - no directories can exist within a repository
4. No version history is currently saved to Pythonista
5. Only python (.py) files can be edited (and therefore changed and committed)

## Contributing
If you'd like to contribute to this library, please fork on github: https://github.com/mmurdoch/githubista

