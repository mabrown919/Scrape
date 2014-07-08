#intelligent philanthropy scraping
#
# fetch the links to PDF-overviews for each charity

#charity search results:
#http://www.intelligentphilanthropy.com/search-results?
#
#next search page:
#http://www.intelligentphilanthropy.com/search-results?original_url[]=search-results&page=XX&sort=`nodes`.name ASC
#url encoded version:
#http://www.intelligentphilanthropy.com/search-results?original_url%5B%5D=search-results&page=2&sort=%60nodes%60.name+ASC

#21 pages total with a maximum of 25 results per page

#subsequent pages from search results:
#http://www.intelligentphilanthropy.com/overview/XXXXXXX-*

#following page w/pdf link:
#http://www.intelligentphilanthropy.com/overview/XXXXXXX-*

#PDF location:
#http://www.intelligentphilanthropy.com/PDFs/YYYY Analytical Overviews/*.pdf

import re
import mechanize
from bs4 import BeautifulSoup
import urllib
import os

baseURL="http://www.intelligentphilanthropy.com"
overviewLinks = []
overviewSubStr = []
overviewPDFlinks = []
pdfLinks = []
downDir = "/Users/apple/Desktop/startup/pi"

#login
br = mechanize.Browser()
uname = "kemar.england@gmail.com"
pword = "8201hrh4thr734rb1no"
br.open("http://www.intelligentphilanthropy.com/login")
br.select_form(nr=1)
br['login'] = uname
br['password'] = pword
br.submit()

#get number of results
srchURL = "http://www.intelligentphilanthropy.com/search-results"
response = br.open(srchURL)
html = response.read()
soup = BeautifulSoup(html)
numResults = len(soup.find_all("div", class_="entry"))
#numResults = 1

dlLinks = []

#loop for pages
for x in range(0,numResults):
	#zero out lists
	overviewLinks = []
	overviewSubStr = []
	prePDFlinks = []
	pdfLinks = []

	x+=1
	response = br.open("http://www.intelligentphilanthropy.com/search-results?original_url%5B%5D=search-results&page="+str(x)+"&sort=%60nodes%60.name+ASC")
	html = response.read()
	soup = BeautifulSoup(html)
	#overviewLinks = []					#fully qualified links; http://www.intelligentphilanthropy.com/overview/268074-a-m-partnership
	#overviewSubStr = []						#just the 'href'; /overview/268074-a-m-partnership
	for links in soup.find_all('h3'):
		for link in links:
			#print link.get('href')		/overview/268074-a-m-partnership
			overviewSubStr.append(link.get('href'))
			overviewLinks.append(baseURL+link.get('href'))
	#print overviewLinks				http://www.intelligentphilanthropy.com/overview/268074-a-m-partnership
	#overviewPDFlinks = []
	for x in range(0,len(overviewSubStr)):
		prePDFlinks.append(baseURL+"/overview-pdf/"+overviewSubStr[x].split("/")[2])
	#print overviewPDFlinks				http://www.intelligentphilanthropy.com/overview-pdf/968230-arab-world-media
	
	# for loop for results within the pages returned
	#pdfLinks = []
	for y in range(0,len(prePDFlinks)):
		print "pre pdf link: " + prePDFlinks[y]
		response = br.open(prePDFlinks[y])
		html = response.read()
		soup = BeautifulSoup(html)
		try:
			pdflnk = soup.find(id="button-pdf-download").a["href"]
			pdfLinks.append(urllib.quote(baseURL+pdflnk.encode('utf-8')))
		except TypeError:
			pdfLinks.append("NO PDF AVAILABLE")
	dlLinks += pdfLinks
#save dl links for later
#outfile
f = open(downDir+"/pdflinks.txt", "w")
f.write("\n".join(dlLinks))
