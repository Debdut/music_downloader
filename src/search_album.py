#!/usr/bin/env python

from webmusic_downloader import create_dir_and_download, sizeof_fmt
from google import search
import sys
import requests
from lxml import html
from lxml.html.clean import clean_html


HEADER = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}

def album_info (album):

    page = requests.get (album[2], headers=HEADER)
    tree = html.fromstring (clean_html (page.content))

    return tree.xpath ('//h1')[0].text

def main ():

    if len (sys.argv) < 2:
        print "Error: Invalid args"
        print "Usage: download_album album_name [Directory]"
        print
        return 0

    sub_string_h = '://webmusic.cc/hindi_music.php?id='
    sub_string_b = '://webmusic.cc/bengali_music.php?id='
    sub_string_e = '://webmusic.cc/english_music.php?id='
    search_term = sys.argv[1] + ' site:webmusic.cc'

    albums = []

    if len(sys.argv) >= 3:
        directory = sys.argv[2]
    else:
        directory = None

    print "\nChoose from following search results :\n"

    for url in search (search_term, stop = 10):

        if sub_string_h in url:
            albums.append ([url.replace (sub_string_h, '').replace ('http', '').replace ('https', ''), 'h', url])
            found = 1

        elif sub_string_b in url:
            albums.append ([url.replace (sub_string_b, '').replace ('http', '').replace ('https', ''), 'b', url])
            found = True

        elif sub_string_e in url:
            albums.append ([url.replace (sub_string_e, '').replace ('http', '').replace ('https', ''), 'e', url])
            found = True

    total_size = 0
    count = 1
    if found:
        for album in albums:
            print str(count)+')', album_info (album)
            count += 1
        print "0)All\n"

        while True:
            try:
                option = int (raw_input ("Enter choice: "))
                if option in range (0, count):
                    break
                else:
                    print "Oops!  That was a invalid choice.  Try again..."
            except ValueError:
                print "Oops!  That was not a number.  Try again..."
        if option in range (1, count):
            print
            total_size += create_dir_and_download ([None, albums[option-1][1], albums[option-1][0], directory])
        elif option == 0:
            for album in albums:
                total_size += create_dir_and_download ([None, album[1], album[0], directory])

        print "\nTotal Download Size:", sizeof_fmt (total_size)
        print

    else:
        print "Album Not Found"
        print

if __name__ == '__main__':
    main ()
