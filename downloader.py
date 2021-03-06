import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import subprocess

def report(count, block_size, total_size):
    """Report save progression."""
    progress_size = int(count * block_size) / (1024 * 1024)
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r  {0}%, {1} MB".format(percent, progress_size))
    sys.stdout.flush()


def save(url, dst, force=False):
    """Download a file at url to local folder."""
    #if not os.path.isfile(dst) or force:
        # Test if the directory exist or create
    d = os.path.dirname(dst)
    if not os.path.exists(d):
        os.makedirs(d)
    print(u"\nDownloading: {0} to {1}".format(url, dst))
        #urllib.urlretrieve(url, dst, report)
    cmd='wget -c -O "%s" "%s"' % (dst,url)
    subprocess.call(cmd,shell=True)

def downloadYear(year):

    url = 'https://developer.apple.com/videos/wwdc' + str(year) +  '/'
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    container = soup.find('section', 'all-content')
    sections = container.find_all('li', 'video-tag session')
    events = container.find_all('li', 'video-tag event hidden')
    for index, section in enumerate(sections, start=0):
        session_string = section.find('span', 'smaller')
        sessionID = session_string.text.split(' ')[1]
        event_string = events[index].find('span', 'smaller').text
        downloadSessionVideo(str(year), event_string, sessionID)

def downloadSessionVideo(year, eventName, sessionID):
    print(year, eventName, sessionID)
    folder_dst = 'WWDC/' + year + '/' + eventName
    url = 'https://developer.apple.com/videos/play/wwdc' + year + '/' + sessionID + '/'

    page = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    title = page.find('title').text.split('-')[0].strip()
    print ('\n\n'+title)
    resource = page.find('ul', 'supplements')
    a = resource.find_all('a')

    for a_href in a:
        if len(a_href) and 'SD' in a_href.text:
            dst = u"{0}/{1}/{2}.mp4".format(folder_dst, title, title)
            save(a_href['href'], dst)

        if len(a_href) and 'PDF' in a_href.text:
            dst = u"{0}/{1}/slides.pdf".format(folder_dst, title)
            save(a_href['href'], dst)

downloadYear(2019)

