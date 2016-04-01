_Based on [wc_sync](https://github.com/pysmath/wc_sync) by pysmath._

## Installation

1. Clone/download this repo to pythonista.
2. Update the INSTALL_PATH variable at the top of Working_Copy_Sync.py, if needed. (Easiest just to install in Documents/wc_sync).
3. Go to Working Copy, Allow URL actions, and copy the URL key.
4. Run Working_Copy_Sync and paste in your URL key from Working Copy.
5. Add to quick actions menu to access from within other files

## Notes

Each action (other than "Clone" Repo) uses your current file and working directory to determine which repo to update in Working Copy. Because of this, repos must live in the home (Documents) directory and cannot be nested under other folders. 

Since Pythonista 2.0 cannot (as of right now) present a view as a sidebar anymore, the view has been changed to a modal. This also provided the opportunity to spell out what each button does. 
