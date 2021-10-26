# GUI for tpdb2xbvr
This project is a gui wrapper as well as scene search that has been built upon tpdb2xbvr by Tweeticoats.  
It can be used to search as well as scrape ThePornDB for scenes that are not found by the scraper or to manually enter scenes that are not found in ThePornDB.  

Tweeticoats program can be found here:  

https://github.com/Tweeticoats/tpdb2xbvr

## Installation

### 1) Create virtual environment  
from project directory, create virtual environment with 

>python -m venv env
### 2) Activate virtual environment
Windows:
> .\env\Scripts\activate  
> 
Unix/macOS  
> source env/bin/activate

### 3) Run "main.py"

##Instructions
Start the webserver, then, either...  

-scrape a scene (see sample URLs below)  
-or use the search function to find a scene, then scrape it  
-or enter your own data into the fields if you can't find a scene online.  
Then click "Export" to copy the JSON location to the clipboard.  
You can then launch XBVR -> Options -> Data import/export  
Paste clipboard contents into "Bundle URL" and click "import content bundle"
![Github](https://user-images.githubusercontent.com/92050698/138786840-3cdaa793-3fad-4658-bfab-f44b2e637886.png)


## Sample URLs to scrape
https://api.metadataapi.net/scenes/wankz-vr-hello-neighbor  
https://api.metadataapi.net/scenes/wankz-vr-wankzvr-car-wash-1  
https://api.metadataapi.net/scenes/wankz-vr-paddys-pub    
https://api.metadataapi.net/scenes/evileyevr-rescue-mission  




# tpdb2xbvr
This script calls the metadataapi.net and generates a json bundle to import scenes manually into xbvr.

## Configuration
Create an account on metadataapi.net and generate an api key.
Edit tpdb2xbvr and update the headers to include this key.

headers= {
     "Authorization": "Bearer xxxxxxxxxx",
     "Content-Type": "application/json",
     "Accept": "application/json"
}


## Running
python3 tpdb2xbvr.py  https://api.metadataapi.net/scenes/virtualrealporn-lara039s-new-friend

1. Copy output.json to a web server.
2. open up the xbvr config
3. import the content bundle.
4. Run any scraper to build the search index
