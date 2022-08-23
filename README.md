# KHInsiderDownloader
Script to download full albums at a time from KHInsider

Will default to downloading FLAC versions of the songs.

However, if FLAC versions are not found, the program will fallback to downloading the MP3 versions instead



Required pip Modules:
```
argparse
bs4 (BeautifulSoup)
html5lib
Requests
urllib3
```

How to use:
```
usage: DownloadScript.py -a ALBUM_LINK

Where album link is the link to the main album page on KHInsider.
```
Example: 
```
python3 DownloadScript.py -a https://downloads.khinsider.com/game-soundtracks/album/mario-kart-8
```
