#test downloading flac from url
import requests
import argparse
import os
from urllib.parse import unquote
from bs4 import BeautifulSoup

album_urls = []

parser = argparse.ArgumentParser(description='Album Downloader')
parser.add_argument('-a', '--album', action='store', nargs = '+', type=str)

args = parser.parse_args()


album_urls.append(args.album[0])

#print(album_urls[0])

#album_url = "https://downloads.khinsider.com/game-soundtracks/album/drifting-lands-original-soundtrack"
#download_url = "https://downloads.khinsider.com/game-soundtracks/album/pokemon-legends-arceus-complete-soundtrack/1-26%2520-%2520Suspense.mp3"


#grab the link to the flac file on the passed in page
def get_flac_link(page_url):
    #response object
    r = requests.get(page_url)
    
    #create soup object
    soup = BeautifulSoup(r.content,'html5lib')
    
    #find all links on page
    links = soup.findAll('a')
    
    #filter links ending w/ .flac
    #and grab what should be the only link ending in flac
    try:
        flac_link = [link['href'] for link in links if link['href'].endswith('flac')][0]
    #If FLAC download not found for an album, fallback to MP3 download instead
    except:
        flac_link = [link['href'] for link in links if link['href'].endswith('mp3')][0]
    
    #return link to flac file
    return flac_link


def get_download_urls(album_url):
    #response object
    r = requests.get(album_url)
    
    #create soup object
    soup = BeautifulSoup(r.content, 'html5lib')
    
    #find all links on page
    #links = soup.find_all(string=re.compile("get_app"))
    links = soup.findAll('a')
    
    #filter links to contain only links from
    #tags that had "get_app" in it
    #AKA, the download button beside each song name on the page
    filtered_links = []
    for link in links:
        if "get_app" in str(link):
            filtered_links.append(link)
    
    
    #Extract the href links from the list of filtered soup links
    page_links = []
    for link in filtered_links:
        page_links.append(link['href'])
    
    
    #return the list of strings with the beginning of the link appended to each item
    return ["https://downloads.khinsider.com" + e for e in page_links]



def download_flacs(flac_links):
    #Let user know of MP3 fallback was used
    if flac_links[0].endswith("mp3"):
        print("\nFLAC download not found, downloading MP3 instead.\n")
    
    #grab name from the link
    for link in flac_links:
        #use unquote to decode the html characters from the link back into ascii characters
        file_name = unquote(link.split('/')[-1])
        print("  Downloading file:%s "%file_name)
        
        #response object
        #turn on stream mode to load file in chunks
        #since by default, it is normally saved as string
        #and some files (FLACS) may be too large to store in a string
        r = requests.get(link, stream = True)
        
        #iterate through chunks
        with open(file_name, 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        print("  %s downloaded.\n"%file_name)
    
    print("All songs downloaded.")
    return



for album_url in album_urls:
    links = get_download_urls(album_url)
    flac_links = []
    for link in links:
        flac_links.append(get_flac_link(link))
    download_flacs(flac_links)
