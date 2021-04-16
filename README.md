# Location Sharing Module (used with Google Location Sharing)
This is third-party module for the inkycal project for release 2.0.0.

This module displays the locations of everyone you are connected with via Google Location Sharing. 

<p align="left">
<img src="https://github.com/emilyboda/inkycal_locationsharing/blob/master/example.PNG" width="300"><img 
</p>

You must follow the instructions these instructions to set it up:
1) Install a chrome extension to download your cookies, like this one :https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid/related.
2) Navigate to Google Maps, and log in (if you aren't already logged in). 
3) Use the extension to download your cookies. 
4) Move the cookies file to your Pi. 
5) Enter the full file path to your cookies file in the box in the settings file web-ui. For example: /home/pi/Inkycal/example.cookies
6) Enter the email address you logged into Google Maps with into the box in the settings file web-ui. For example: myemail@gmail.com

# Installation instructions
How to install the module.

1) Navigate to the modules directory
`cd Inkycal/inkycal/modules`

2) Download the third-party module:
```bash
# The URL is the rawfile url. e.g. open mymodule.py, then click on [raw] to see the rawfile-url
wget https://raw.githubusercontent.com/emilyboda/inkycal_locationsharing/master/inkycal_locationsharing.py
```

3) Register this module in Inkycal
```python3
# In python, type the following commands:
from inkycal import Inkycal
Inkycal.add_module('/full/path/to/your/module.py')
# If everything went well, you should see a printed message without red lines.
```

# Configuring this module
Once the module is registered, navigate to `Inkycal/server` and run the flask-server with:
`flask run --host=0.0.0.0`

The web-UI should now be available at `http://raspberrypi.local:5000/`. If this does not work, you can manually use the IP address instead: `http://192.168.1.142:5000/`

Copy the generated settings.json file to your raspberry Pi (VNC/ WinSCP). 
If you don't have access to the Raspberry Pi via VNC/ WinSCP, you can copy the settings.json file to the microSD card instead. After inkycal starts, it will use the new settings.json file.

# How to remove this module
```python3
# In python, run the following commands:
from inkycal import Inkycal
Inkycal.remove_module('filename.py') # where filename.py is the name of your third-party module in Inkycal/inkycal/modules
# If everything went well, you'll see a printed message without red lines.
```
