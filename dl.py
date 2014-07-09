import re
import mechanize
from bs4 import BeautifulSoup
import urllib
import os
import time

downDir = "/Users/apple/Desktop/startup/pi/"

#login
br = mechanize.Browser()
uname = "kemar.england@gmail.com"
pword = "8201hrh4thr734rb1no"
br.open("http://www.intelligentphilanthropy.com/login")
br.select_form(nr=1)
br['login'] = uname
br['password'] = pword
br.submit()

inf = open(downDir+"pdflinks.txt", "r")
for line in inf:
	url = line.strip()
	print "url is: ", url
	goodurl = urllib.unquote(url)
	br.retrieve(goodurl,downDir+urllib.unquote(url).split("/")[-1])
	time.sleep(1)
