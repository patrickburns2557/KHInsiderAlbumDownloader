#test downloading flac from url
import requests
import argparse
import os
import sys
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup

album_urls = []
current_album = ''
total_downloads = 0
multiple_discs = False
want_multiple_discs = False

parser = argparse.ArgumentParser(description='KHInsider Album Downloader')
parser.add_argument('-a', '--album', action='store', nargs = '+', type=str)
parser.add_argument('-f', '--file', action='store', nargs = '+', type=str, help="input file with album links on each line")
parser.add_argument('-d', '--discs', action='store_true', help="Add if you want the program to download albums with multiple discs into separate disc folders")

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

#Check if user wants to separate album with multiple discs into separate disc folders
want_multiple_discs = args.discs


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
    global multiple_discs
    #response object
    r = requests.get(album_url)
    
    #create soup object
    soup = BeautifulSoup(r.content, 'html5lib')
    
    #TEST IF AN ALBUM CONTAINS MULTIPLE DISCS
    multiple_discs = False
    #Find all <b></b> strings on page
    bList = soup.findAll('b')
    #test if "CD" is in this list
    for b in bList:
        if "CD" in str(b):
            multiple_discs = True
    #print("Multiple discs: " + str(multiple_discs))
    #print("Want multiple discs: " + str(want_multiple_discs))
    
    #find all links on page
    #links = soup.find_all(string=re.compile("get_app"))
    links = soup.findAll('a')
    
    #Grab and save name of current album to create a subfolder for it when downloading starts
    current_album = soup.find('h2').string
    #replace any illegal filename characters with underscores
    current_album = current_album.replace('\\', '_').replace('/', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    
    
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
    global total_downloads
    global multiple_discs
    global want_multiple_discs
    #Let user know of MP3 fallback was used
    if flac_links[0].endswith("mp3"):
        print("\nFLAC download not found, downloading MP3 instead.\n")
    
    #put each album into its own subfolder
    os.mkdir(current_album)
    
    
    #grab name from the link
    for link in flac_links:
        #use unquote to decode the html characters from the link back into ascii characters
        file_name = unquote(link.split('/')[-1])
        #replace any illegal filename characters with underscores
        file_name = file_name.replace('\\', '_').replace('/', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        #file_directory = unquote(link.split('/')[-1]) + current_album
        print("  Downloading file:%s "%file_name)
        
        #response object
        #turn on stream mode to load file in chunks
        #since by default, it is normally saved as string
        #and some files (FLACS) may be too large to store in a string
        r = requests.get(link, stream = True)
        
        #If there are multiple discs in the album, AND the user wants them separated, create disc subfolders for the album and download the files there
        if multiple_discs and want_multiple_discs:
            directory = (current_album + "/" + "Disc " + re.sub("[^0-9]", "", file_name[0:2])) #re.sub portion removes any non-numeric characters from the string
            #check if the disc directory exists or not before creating it
            if not os.path.exists(directory):
                os.mkdir(directory)
        #otherwise, just create a single directory for each album
        else:
            directory = (current_album)
            if not os.path.exists(directory):
                os.mkdir(directory)
        
        
        #iterate through chunks
        with open((directory + "/" + file_name), 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        print("  %s downloaded.\n"%file_name)
        total_downloads += 1
    
    print("All songs downloaded.")
    return


print("Downloading " + str(len(album_urls)) + " albums...")
for album_url in album_urls:
    links = get_download_urls(album_url)
    flac_links = []
    for link in links:
        flac_links.append(get_flac_link(link))
    download_flacs(flac_links)

print("\n\n" + str(total_downloads) + " songs downloaded successfully.")
