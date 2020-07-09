#!/usr/bin/env python3
# gcxml.py
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

from lxml import etree

with open('sitemap.xml', 'r') as f:
    gcxml = f.read().encode('utf-8')

parser = etree.XMLParser(encoding='utf-8')
tree = etree.fromstring(gcxml, parser=parser)
locs = tree.findall('url/loc')
allcomics = []
for loc in locs:
    url = loc.text
    if '/comics' not in url:
        comicname = url[24:]
        if comicname:
            allcomics.append(comicname)

with open('allcomics.txt', 'w') as f:
    for comicname in sorted(allcomics):
        f.write(comicname)
        f.write('\n')

