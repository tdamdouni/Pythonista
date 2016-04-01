# Pythonista Tools Installer

A front-end UI program to browse and/or download scripts listed on 
[Pythonista-Tools](https://github.com/Pythonista-Tools/Pythonista-Tools).

## Installation
To install the program, copy and run following one-line python statements 
in Pythonista interactive prompt. It saves the `ptinstaller.py` file
to the current working directory.

```python
import requests as r; o=open('ptinstaller.py','w'); o.write(r.get('http://j.mp/pt-i').text); o.close()
```

## Usage
Execute the saved `ptinstaller.py` program to launch the UI. Follow the 
on-screen instruction to browse and install/uninstall scripts. The scripts are by default installed under **`~/Documents/bin/`**.

### Screenshots

![1](https://cloud.githubusercontent.com/assets/2344308/9724048/58480568-5614-11e5-9403-d986adf82727.JPG) ![2](https://cloud.githubusercontent.com/assets/2344308/9724050/5e3736e2-5614-11e5-95ba-7333ec7c952d.JPG)
