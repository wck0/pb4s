from lxml import html
import requests

imgtag = "og:image"
url = "http://www.gocomics.com/pearlsbeforeswine/"

page = requests.get(url)
tree = html.fromstring(page.content)

mm = tree.xpath('//meta[@property="og:image"]')
comicurl = mm[0].items()[1][1]
comic = requests.get(comicurl)

filename = comic.headers['Content-Disposition']
filename = filename[filename.index('"')+1:-1]

with open(filename, 'wb') as f:
    for chunk in comic:
        f.write(chunk)
        
