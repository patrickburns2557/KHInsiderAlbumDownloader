#test downloading flac from url
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup

album_url = "https://downloads.khinsider.com/game-soundtracks/album/drifting-lands-original-soundtrack"
download_url = "https://downloads.khinsider.com/game-soundtracks/album/pokemon-legends-arceus-complete-soundtrack/1-26%2520-%2520Suspense.mp3"


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
    flac_link = [link['href'] for link in links if link['href'].endswith('flac')][0]
    
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
    #grab name from the link
    for link in flac_links:
        #use unquote to decode the html characters from the link back into ascii characters
        file_name = unquote(link.split('/')[-1])
        print(  "Downloading file:%s "%file_name)
        
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
        
        print(  "%s downloaded.\n"%file_name)
    
    print("All songs downloaded.")
    return




links = get_download_urls(album_url)
flac_links = []
for link in links:
    flac_links.append(get_flac_link(link))

download_flacs(flac_links)