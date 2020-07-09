# pb4s

This script fetches and saves an image of a comic from gocomics.com

You can call it with options to specify which comic and date you want.
For example, running the program as
`pb4s.py -c nameofthecomicstrip -d YYYYMMDD`
will go and grab the strip located at

http://www.gocomics.com/nameofthecomicstrip/YYYY/MM/DD

By default, `-c` is `pearlsbeforeswine` and `-d` is today.

The motivation for creating this script is the following: up until January
2017, gocomics.com supported RSS feeds for each of the comics it hosts.
The site also underwent a redesign around the same time.
I wanted a way to see the comic without having to look at all the extra
cruft on the page.

The script requires the lxml, requests, and Pillow python libraries, which you can
install by doing
`pip3 install lxml`
`pip3 install requests`
`pip3 install Pillow`

# TODO
* make it all more object oriented, with something like a `comic` object 
that has methods to do all the downloading, converting file types, displaying, 
etc.


