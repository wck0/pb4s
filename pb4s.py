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

from lxml import html
import requests

imgtag = "og:image"

# change the url below to match the comic you want. I rather like Pearls
# Before Swine by Stephan Pastis.
url = "http://www.gocomics.com/pearlsbeforeswine/"

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

# the file name of the comic image is contained in the headers of the request
# data. comic.headers is a dictionary, and we want the value for the
# 'Content-Disposistion' key, which will be a string like 
# 'inline; filename="pb170702.jpg"'
# we parse that string and grab the portion between the double quotes
filename = comic.headers['Content-Disposition']
filename = filename[filename.index('"')+1:-1]

# finally, write the comic image to a file.
# note: it seems to be a jpg on Sundays, and a gif all the other days
with open(filename, 'wb') as f:
    for chunk in comic:
        f.write(chunk)
        
