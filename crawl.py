#!/usr/bin/python

#charity navigator
#num=5200
#http://www.charitynavigator.org/index.cfm?bay=search.summary&orgid=+num+#.U2Kwz14T3IZ
#http://www.charitynavigator.org/index.cfm?bay=search.summary&orgid=3293#

url="http://www.charitynavigator.org/index.cfm?bay=search.alpha"

import string, urllib, os, sys
from bs4 import BeautifulSoup
import io

page = urllib.urlopen(url).read()
soup = BeautifulSoup(page)

#a-z directory url index 
urldirectory = [] 
for link in soup.find(id="maincontent2").p.find_all('a'):
	urldirectory.append(link.get('href'))
# with open("urldirectory.txt", 'w') as urldf:
# 	for link in urldirectory:
# 		urldf.write(str(link)+"\n")
# urldf.close()

#a-z directory list
urllist = []
for link in soup.find(id="maincontent2").find_all('a', recursive=False):
	urllist.append(link.get('href'))
# with open("a"+".txt", 'w') as urlfile:
# 	for link in urllist:
# 		urlfile.write(str(link)+"\n")

for link in urldirectory:
	page = urllib.urlopen(link).read()
	soup = BeautifulSoup(page)
	#split the end link on the end from "cn" and add .txt
	fh = io.open(link.split("=")[-1]+".txt", 'w', encoding="utf-8")
	for l in soup.find(id="maincontent2").find_all('a', recursive=False):
		#print l
		fh.write(l.string+": "+l['href']+"\n")
fh.close()
