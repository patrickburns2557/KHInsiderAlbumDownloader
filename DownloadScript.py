#test downloading flac from url
import requests
import argparse
import os
import sys
from urllib.parse import unquote
from bs4 import BeautifulSoup

album_urls = []
current_album = ''

parser = argparse.ArgumentParser(description='KHInsider Album Downloader')
parser.add_argument('-a', '--album', action='store', nargs = '+', type=str)
parser.add_argument('-f', '--file', action='store', nargs = '+', type=str, help="input file with album links on each line")

args = parser.parse_args()

#print out help message if no arguments given
if not len(sys.argv)>1:
    parser.print_help(sys.stderr)
    sys.exit(1)

#Add albums to album_urls list
if args.album is not None:
    album_urls.append(args.album[0])
if args.file is not None:
    #if an input file is given, read it line by line and add to the list
    lines = []
    with open(args.file[0]) as file:
        lines = file.readlines()
    for line in lines:
        album_urls.append(line.rstrip())


#for a in album_urls:
#    print(a)


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
    global current_album
    #response object
    r = requests.get(album_url)
    
    #create soup object
    soup = BeautifulSoup(r.content, 'html5lib')
    
    #find all links on page
    #links = soup.find_all(string=re.compile("get_app"))
    links = soup.findAll('a')
    
    #Grab and save name of current album to create a subfolder for it when downloading starts
    current_album = soup.find('h2').string
    
    
    
    print("\n\nDownloading album: " + current_album)
    
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
    
    #put each album into its own subfolder
    os.mkdir(current_album)
    
    
    #grab name from the link
    for link in flac_links:
        #use unquote to decode the html characters from the link back into ascii characters
        file_name = unquote(link.split('/')[-1])
        
        #file_directory = unquote(link.split('/')[-1]) + current_album
        print("  Downloading file:%s "%file_name)
        
        #response object
        #turn on stream mode to load file in chunks
        #since by default, it is normally saved as string
        #and some files (FLACS) may be too large to store in a string
        r = requests.get(link, stream = True)
        
        #iterate through chunks
        with open((current_album + "/" + file_name), 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        print("  %s downloaded.\n"%file_name)
    
    print("All songs downloaded.")
    return


print("Downloading " + str(len(album_urls)) + " albums...")
for album_url in album_urls:
    links = get_download_urls(album_url)
    flac_links = []
    for link in links:
        flac_links.append(get_flac_link(link))
    download_flacs(flac_links)
