import sys, re
from HTMLParser import HTMLParser
import urllib, urlparse

arglen = len(sys.argv)
if arglen < 2 or arglen > 3:
	print """   Error\n   Usage: python webcrawler.py URL [max_urls_to_parse]\n   <<Max_urls_to_parse>> is optional """
	sys.exit()
elif arglen==2:	# Only url is passed as argument
	url = sys.argv[1]
elif arglen==3:	# 2 arguments are passed: url, and max no. of urls to parse before stopping
	url = sys.argv[1]
	urllimit = int(sys.argv[2])

temp = []

# Check if provided url contains text/html
if re.search('text/', urllib.urlopen(url).headers.getheader('content-type')):
	print 'URL valid.'
else:
	print 'Invalid URL.'
	sys.exit()

for line in urllib.urlopen(url):
	temp.append(line)

page = ''.join(temp)

class LinkParser(HTMLParser):
	temp = []
	def handle_starttag(self, tag, attrs):
		if tag=='a' and attrs[0][0]=='href':
			link = attrs[0][1]
			if not re.search('^http:', link):
				link = urlparse.urljoin(url, link)
			self.temp.append(link)
	def get(self):
		return self.temp

parser = LinkParser()
masterList = []
processedList = []

def getLinks(htmlText):
	parser.feed(htmlText)
	links = parser.get()
	for link in links:
		if link not in masterList:
			masterList.append(link)

	for link in masterList:
		if link not in processedList:
			if arglen == 3 and len(processedList) > urllimit-1:
				return
			else:
				processedList.append(link)
		else:
			continue

		if re.search('text/', urllib.urlopen(link).headers.getheader('content-type')):
			print 'Processing...', str(link)
			array = []
			for line in urllib.urlopen(link):
				array.append(line)
			docText = ''.join(array)
			getLinks(docText)
		else:
			print 'Ignoring non text/html link...', str(link)
	return True	

try:
	result = getLinks(page)
	if result==True:
		print 'Done.'
except Exception:
	print 'Exception caught...exiting.'
	sys.exit()
