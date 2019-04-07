import bs4 as bs
import urllib
import urllib2
# from HTMLParser import HTMLParser


response = urllib2.urlopen("https://pythonprogramming.net/parsememcparseface/")
html = response.read()

soup = bs.BeautifulSoup(html, 'html.parser')

i = 1
for img in soup.findAll('img'):
	temp = img.get('src')
	if temp[:1] == "/":
		image = "https://pythonprogramming.net/parsememcparseface/" + temp
	else:
		image = temp
	
	nametemp = img.get('alt')
	if nametemp == None:
		filename = str(i)
		i += 1
	else:
		filename = nametemp
		
	try:
		imagefile = open(filename + ".jpeg", "wb")
		imagefile.write(urllib2.urlopen(image).read())
		imagefile.close()
	except:
		pass