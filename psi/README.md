# Pythonista Script Index

Script search, installation and removal made easy in Pythonista.

Proof-of-Concept project to setup a central Index for Pythonista Scripts. 
The Index acts as a server to provide necessary information for a client
program to manage search, installation and un-installation in Pythonista.
Such a proof-of-concept client is psiclient ([Gist
link](https://gist.github.com/ywangd/184b9e0e1e76d8b92063) or [GitHub
repo](https://github.com/ywangd/psiclient)). 

Note: It is currently in test phase and very primitive. Suggestions are welcome.

## Basic structure
Two JSON files are required for the index to work, the Main Index file and the
Script Definition file.
* **Main Index File**
  ([index.json](https://github.com/ywangd/pythonista-script-index/blob/master/index.json))
    - It only has minimal information of each script, including the
      script's short name, description and url pointing to the script's index file.
* **Script Definition File**
  ([scripts.json](https://github.com/ywangd/pythonista-script-index/blob/master/scripts.json)
  for an example)
    - It contains detailed information about a script, e.g. versions, and its
      actual download url.


## Examples
**NOTE**: Comments are for demostration purpose only and are NOT allowed in
actual files.

A sample excerpt of the **Main Index File** could be as follows:
```javascript
{
    "meta_version": "1.0",  // version of this main index file
    "name": "Pythonista Script Index",  // name of the main index
    "website": "https://github.com/...",  // url to the main index repo or website

    "scripts": {
        "A_script": {
            "meta_url": "https://github.com/person/repo/info.json", // url to the script definition file
        },

        "B_script": {
            "meta_url": "https://github.com/someone/somerepo/info.json#B_script",
        }
    }
    
}
```

And a sample **Script Definition File** is as follows:
```javascript
{
    // Version of this index file
    // It tells a client program how this index file shall be parsed and allows
    // versioning of the index file itself
    "meta_version": "1.0",  
    "name": "An awesome script",  // script full name
    "author": "First Last",
    "email": "email@test.com",
    "website": "https://...",  // url to script's repo or website
    "description": "he is too awesome",

    "releases": [ 
        {
            "version": "1.0", 
            "url": "https://.../a_script.py" // url to download version 1.0 of the script
            // Note: the client should always try to download a same-name pyui file
        },

        {
            "version": "2.0", 
            "url": "https://.../a_script.zip"  // url to download version 2.0 of the script
        },
    ]
}
```

The **Script Definition File** allows authors to keep almost all maintenance
information in their own repos and provide its own versionings. Also note many
of these information are optional except `url`.

Note the use of `meta_version` for representing the version number of the
index file itself. This allows future changes to the JSON file structure
without breaking old index files, i.e. any future changes will receive a new
version number. The first thing a client program does is to check the meta_version which
tells the client program what structure to expect from the index file.

In the **Main Index File**, note the use of `#B_script` tag for the second
script. This allows multiple scripts to share a single **Script Definition File**:
```javascript
{
    "script1": {
        // ...
    },

    "B_script": {

        "meta_version": "1.0",  
        "name": "B Script",  // script full name
        "author": "First Last",
        "email": "email@test.com",
        "website": "https://...",  // url to script's repo or website
        "long_description": "...",

        "releases": [ 
            {
                "url": "https://....", 
                // ...
            }
        ]
    }, 

    "script3": {
        // ...
    }
}
```

The current supportted file types are:
* Single Python file - it is simply copied to the destination folder
    * The client should always check whether a same name pyui file is available
      at the same url and download it if one exists.
* Single zip file - all contained files are extracted into a folder and place
  into the destination folder

