A set of four scripts for cleaning the status bar of iOS screenshots. Cleaning consists of setting the battery and signal strength icons to full and showing Bluetooth and Location Services as on. The four scripts are:

* **Cleanbar.py** Cleans a single screenshot taken when the device was on WiFi. This script includes the class and function definitions necessary for all the scripts and is called as a module by the others.
* **Cleanbar Pair.py** Cleans two screenshots taken when the device was on WiFi and puts them side by side.
* **Cleanbar LTE.py** Cleans a single screenshot taken when the device was on LTE.
* **Cleanbar LTE Pair.py** Cleans two screenshots taken when the device was on LTE and puts them side by side.

For each script, the user is presented with the images in the Camera Roll and is expected to choose one or two. When the cleaning is done, the resulting image is displayed in the Pythonista console, from which it can be copied or saved to the Camera Roll.

