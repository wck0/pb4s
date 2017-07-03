# pb4s

This script fetches and saves an image of a comic from gocomics.com
Without modification, it only gets the comic for the current day.
It would be easy to change the url to get a comic for a particular date,
since gocomics uses the following structure:
http://www.gocomics.com/nameofthecomicstrip/YYYY/MM/DD

The motivation for creating this script is the following: up until January
2017, gocmics.com supported RSS feeds for each of the comics it hosts.
The site also underwent a redesign around the same time.
I wanted a way to see the comic without having to look at all the extra
cruft on the page.

The script requires the lxml and requests python libraries, which you can
install by doing
`pip3 install lxml`
`pip3 install requests`
or use `pip` instead if you are using python2

The script should work fine for both python2 and python3.
No error handling of any sort is implemented, but might be introduced in the
future.
