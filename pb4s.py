#!/usr/bin/env python3
# pb4s.py
# 
# MIT License
# 
# Copyright (c) 2017 William Kronholm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, os
import argparse
import datetime

from lxml import html
import requests

def getcomic(comicname, date=None):
    imgtag = "og:image"    
    url = 'http://www.gocomics.com/' + comicname + '/'
    if date and validdate(date):
        YYYY = date[:4]
        MM = date[4:6]
        DD = date[6:]
        url += YYYY + '/' + MM + '/' + DD
    else:
        today = datetime.datetime.today()
        suffix = today.strftime("%Y/%m/%d")
        url += suffix
    page = requests.get(url)
    
    # we want to parse the page content in a nice way.
    tree = html.fromstring(page.content)
    
    # the url for the comic image is specified in the header, in a meta tag with
    # attribute property="og:image", but we want the url which is given by the
    # content attribute of the same tag
    mm = tree.xpath('//meta[@property="og:image"]')
    
    # mm is a list with one item: a single Element meta.
    # mm[0].items() gives a list of the meta tag attributes, each of which is
    # itself a tuple. For our tag, mm[0].items() is the following:
    # ('property', 'og:image'), ('content', url to comic image file)
    # The url we want is in the content attribute.

    comicurl = mm[0].items()[1][1]
    comic = requests.get(comicurl)
    return comic

def savecomic(comic):
    # comic should be a Response object, i.e. the result of doing a
    # requests.get of some url.
    # the file name of the comic image is contained in the headers of the request
    # data. comic.headers is a dictionary, and we want the value for the
    # 'Content-Disposistion' key, which will be a string like 
    # 'inline; filename="pb170702.jpg"'
    # we parse that string and grab the portion between the double quotes
    filename = comic.headers['Content-Disposition']
    filename = filename[filename.index('"')+1:-1]

    # finally, write the comic image to a file.
    # note: it seems to be a jpg on Sundays, and a gif all the other days
    dirname = filename[:2]
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    with open(dirname + "/" + filename, 'wb') as f:
        for chunk in comic:
            f.write(chunk)
    print("saved file", dirname + "/" + filename)
    return dirname + "/" + filename

def convert2png(filename):
    from PIL import Image
    im = Image.open(filename)
    pngfilename = filename[:filename.rfind('.')] + ".png"
    im.save(pngfilename)
    print("Saved file", pngfilename)
    return pngfilename

def validdate(date):
    try:
        datetime.datetime.strptime(date, "%Y%m%d")
        return True
    except ValueError:
        return False

def listcomics():
    with open('allcomics.txt', 'r') as f:
        allcomics = f.readlines()
    for comicname in sorted(allcomics):
        print(comicname.rstrip())

def main():
    parser = argparse.ArgumentParser(prog='pb4s',
                                     description="Download a comic from gocomics.com"
                                    )
    parser.add_argument('-c', '--comicname',
                        nargs='?',
                        help='name of comic to download',
                        const='pearlsbeforeswine',
                        default='pearlsbeforeswine'
                       )
    parser.add_argument('-d', '--date',
                        nargs='?',
                        help='date of comic to download in YYYYMMDD format'
                       )
    parser.add_argument('-l', '--list-comic-names',
                        action='store_true',
                        dest='listthem',
                        help='List all available comic names. There are a lot of them.'
                       )
    parser.add_argument('-o', '--open-comic',
                        action='store_true',
                        dest='opencomic',
                        help='Open the comic after downloading it.'
                       )
    args = parser.parse_args()
    
    if args.listthem:
        listcomics()
        sys.exit()
    
    if args.comicname:
        comicname = args.comicname
    else:
        comicname = 'pearlsbeforeswine'
    if args.date:
        date = args.date
        if not validdate(date):
            print("Invalid date.")
            parser.print_help()
            sys.exit()
    else:
        date = None
    
    try:
        comic = getcomic(comicname, date=date)
    except Exception as e:
        print("Unable to download comic.")
        print(e)
        sys.exit()
        
    if comic.status_code == 200:
        savedFile = savecomic(comic)
        pngfilename = convert2png(savedFile)
        if args.opencomic:
            os.system('eog ' + pngfilename)
        sys.exit()
    else:
        print("Received status code", comic.status_code)
        print("Exiting")
        sys.exit()

if __name__ == '__main__':
    main()
