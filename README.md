# GUI for tpdb2xbvr
This project is a gui wrapper for tpdb2xbvr by Tweeticoats for ThePornDB (https://metadataapi.net/).  Scene search functionality has also been added.

The program is useful for the following:
* Scrape scenes from ThePornDB that are not found in XBVR.  Then import into XBVR.
* Search for scenes from ThePornDB from within the GUI (then scrape them).  Then Import into XBVR.
* Manually enter a scene to be imported into XBVR, even if it doesn't exist in ThePornDB.  Add your own cover, gallery image, url, tags, etc.

![Github3](https://user-images.githubusercontent.com/92050698/138799895-7ccd2f91-03ed-4619-befd-f3b5a1eca47c.png)

Tweeticoats awesome program can be found here:  

https://github.com/Tweeticoats/tpdb2xbvr

## Installation

### 1) Create virtual environment

from project directory, create virtual environment with 
Windows:
>python -m venv env
> 
Unix/macOS:
>python3 -m venv env

### 2) Activate virtual environment
Windows:
> .\env\Scripts\activate  
> 
Unix/macOS  
> source env/bin/activate

### 3) Install requirements
Windows:
> python -m pip install -r requirements.txt
> 
Unix/macOS  
> python3 -m pip install -r requirements.txt

### 4) Run "main.py"
Windows:
> python main.py
>
Unix/macOS:
> python3 main.py

## Configuration
Create an account on ThePornDB at https://metadataapi.net and generate an api key.
You can paste this key in the GUI and save your configuration with "Save Config".

## Instructions
Click "Start Webserver" (or run your own), then, either...  

* scrape a scene from ThePornDB (see sample URLs below)  
* or use the search function to find a scene on ThePornDB, then scrape it  
* or manually enter your own data into the fields if you can't find a scene online.

Then click "Export" to copy the JSON location to the clipboard.  This will create your import file.

You can then launch XBVR -> Options -> Data import/export  
Paste clipboard (CTRL-V or CMD-V) contents into "Bundle URL" and click "import content bundle" in XBVR.

You'll want to run any scraper in XBVR after you have imported the scene in order for XBVR to recognize the new scene.


## Sample URLs to scrape
https://api.metadataapi.net/scenes/wankz-vr-hello-neighbor  
https://api.metadataapi.net/scenes/wankz-vr-wankzvr-car-wash-1  
https://api.metadataapi.net/scenes/wankz-vr-paddys-pub    
https://api.metadataapi.net/scenes/evileyevr-rescue-mission  

## Additional Search Info
The best way to search is to select a studio by clicking a studio button, then input keywords in the search bar and click "submit".

Search Example:  
* click "vrcosplayx"  
* type: "pokemon" in search 
* click "submit" (or press Enter)  

Results
> vr-cosplay-x-pokemon-officer-jenny-a-xxx-parody  
> vr-cosplay-x-pokemon-team-rocket-jessie-a-xxx-parody

## Development  
I am a python noob.  Pull requests, code cleanup, and any pointers welcome.  This is still buggy, I'm learning python as I go.

### Tests
The tests are incomplete but cover some class methods and functions.  



