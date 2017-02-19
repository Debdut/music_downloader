#!/usr/bin/env python

from lxml import html
from lxml.html.clean import clean_html
import requests
import sys
import os

HEADER = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}


def check_album (language, album_number):

    album_url = "http://webmusic.cc/"+language+"_music.php?id="+album_number
    page = requests.get (album_url, headers=HEADER)
    tree = html.fromstring (clean_html (page.content))

    h1_node_list = tree.xpath ('//h1')
    if len (h1_node_list) == 0:
        return False

    return True

def download_album (language, album_number):

    total_size = 0

    if not check_album (language, album_number):
        print "\n Album not Found!\n"
        return 0

    album_url = "http://webmusic.cc/"+language+"_music.php?id="+album_number
    page = requests.get (album_url, headers=HEADER)
    tree = html.fromstring (clean_html (page.content))

    album_name = tree.xpath ('//h1')[0].text
    print "\nDownloading Album:", album_name

    directory = album_name.replace (' ', '_').replace ('-', '').replace ('__', '_')
    if not os.path.exists (directory):
        os.mkdir(directory)
    os.chdir (directory)

    songs = tree.xpath ('//div[@id="lFs"]/p/a')
    for song in songs:
        total_size += download_song (song.attrib['href'], song.text)

    os.chdir ('..')

    print
    print "-"*53
    print "-"*53
    print "\nDownloaded", len(songs), "songs"
    print "Album Size :", sizeof_fmt (total_size)
    print
    print "-"*53
    return total_size

def download_song (link, name):

    total_length = 0

    print "\n\n> Downloading song: ", name, '\n'

    download_page = requests.get (link, headers=HEADER)
    tree = html.fromstring (clean_html (download_page.content))
    download_link = tree.xpath ('//a[@class="two"]')[0].attrib['href']
    file_ext = download_link.split('.')[-1]
    file_name = (name.replace (' ', '-') + '.' + file_ext).replace ('-.', '.')

    print "GET :", download_link

    with open (file_name, "wb") as f:
        response = requests.get (download_link, stream = True, headers=HEADER)
        total_length = response.headers.get ('content-length')

        if total_length is None:
            f.write (response.content)
        else:
            dl = 0
            total_length = int(total_length)
            print 'SIZE :', sizeof_fmt (total_length), '\n'
            for data in response.iter_content (chunk_size = 4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write ("\r[%s>%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush ()
    print

    return total_length

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def create_dir_and_download (args_list):

    if args_list[1] == 'b':
        language = 'bengali'
    elif args_list[1] == 'h':
        language = 'hindi'
    elif args_list[1] == 'e':
        language = 'english'
    else:
        print "\nError: Enter valid language: b, h, e\n"

    if len (args_list) >= 4 and args_list[3] != None:
        directory = args_list[3]
        if not os.path.exists (directory):
            os.mkdir(directory)
        os.chdir (directory)

    return download_album (language, args_list[2])

def main ():

    create_dir_and_download (sys.arv)
    return 0

if __name__ == '__main__':
    main ()
