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
Single album at a time: DownloadScript.py -a ALBUM_LINK

Where album link is the link to the main album page on KHInsider.


Multiple albums from file: DownloadScript.py -f FILE_NAME.EXT

Where the input file contains 1 album link per line
```
Example: 
```
>python DownloadScript.py -a https://downloads.khinsider.com/game-soundtracks/album/mario-kart-8

>python DownloadScript.py -f input.txt
```
