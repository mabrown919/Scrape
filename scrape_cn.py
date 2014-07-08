#!/usr/bin/python
#scrape
import string, urllib, os, sys
from bs4 import BeautifulSoup
import io
import re
import sqlite3
import time
from pprint import pprint

def getVal(htmltext, pos=0):
	if pos == 0:
		return soup.find("td", text=re.compile(htmltext)).next_sibling.next_sibling.string
	else:
		return soup.find(text=htmltext).find_previous("tr").contents[pos].string.strip()

def popDB(sqllist, tname):
	sql = '''INSERT INTO ''' + tname + ''' VALUES (''' + \
			"?," * (len(sqllist) - 1) + '''?)'''
	cursor.execute(sql, sqllist)
	conn.commit()

fo = open(sys.argv[1])
for line in fo:
	url = line.split()[-1]
	print url

	#url="http://www.charitynavigator.org/index.cfm?bay=search.summary&orgid=6082"
	#url = "http://www.charitynavigator.org/index.cfm?bay=search.summary&orgid=6064"
	#url = "http://www.charitynavigator.org/index.cfm?bay=search.summary&orgid=11257"

	page=urllib.urlopen(url).read()

	soup = BeautifulSoup(page)

	if soup.find("span", text="[DONOR ADVISORY]"):
		print "skipped"
		continue

	# parse objects that will be input into sql DB
	tagline = soup.find("h2", class_="tagline").string
	category = soup.find("p", class_="crumbs").string
	chaNam = soup.find("h1", class_="charityname").string

	EXPENSES_tr = soup.find("a", class_="glossary", text="EXPENSES").find_previous("tr")
	proExp = EXPENSES_tr.find_next("tr").contents[3].string
	admExp = EXPENSES_tr.find_next("tr").find_next("tr").contents[3].string
	funExp = EXPENSES_tr.find_next("tr").find_next("tr").find_next("tr").contents[3].string

	conGifGran = soup.find("td", text=re.compile("Contributions,")).next_sibling.next_sibling.string

	totCon = soup.find(text="Total Contributions").find_previous("tr").contents[3].string

	#time.sleep(1)
	#mission = soup.find("h2", text="Mission").find_next_sibling("p").string
	mmission = soup.find("a", text="Mission").find_previous("h2").find_next("p").stripped_strings
	mission = " ".join(mmission)

	othRev = soup.find("a", class_="glossary", text="Other Revenue").find_previous("tr").contents[3].string

	totPriRev = soup.find("a", class_="glossary", text="Total Primary Revenue").find_previous("tr").contents[3].string

	worCapRat = soup.find("a", class_="glossary", text="Working Capital Ratio").find_previous("tr").contents[5].string

	fedCam = soup.find("td", text=re.compile("Federated Campaigns")).next_sibling.next_sibling.string

	excDef = soup.find("a", class_="glossary", text="Excess (or Deficit)").find_previous("tr").contents[3].string

	memDue = soup.find("td", text=re.compile("Membership Dues")).next_sibling.next_sibling.string

	totRev = getVal("TOTAL REVENUE")

	priRevGro = getVal("Primary Revenue Growth", 5)

	funEve = getVal("Fundraising Events")

	funExpPercent = getVal("Fundraising Expenses", 5)

	govGra = getVal("Government Grants")

	funEff = getVal("Fundraising Efficiency", 5)

	#ha
	netAss = getVal("Net Assets", 3)

	proSerRev = getVal("Program Service Revenue")

	finScore = getVal("Financial")

	proExpPercent = getVal("Program Expenses", 5)

	accTraScore = getVal("Accountability & Transparency")

	payAff = getVal("Payments to Affiliates")

	proExpGro = getVal("Program Expenses Growth", 5)

	relOrg = getVal("Related Organizations")


	finPerMetricst = [None, proExp, admExp, funExp, 
						priRevGro, proExpGro, worCapRat,
						funEff ]

	incStatementt = [None, conGifGran, fedCam, memDue,
					funEve, relOrg, govGra, 
					totCon, proSerRev, totPriRev,
					totRev, proExp, admExp,
					funExp, payAff, excDef,
					netAss]

	infot = [None, tagline, category, chaNam]

	missiont = [None, mission]

	overallt = [None, finScore, accTraScore]

	# put all data objects into the DB
	conn = sqlite3.connect('cn.db')

	cursor = conn.cursor()

	popDB(missiont, "mission")
	popDB(finPerMetricst, "finPerMetrics")
	popDB(incStatementt, "incStatement")
	popDB(infot, "info")
	popDB(overallt, "overall")
	conn.close()

	#time.sleep(1)
"""
delete from finPerMetrics;    
delete from sqlite_sequence where name='finPerMetrics';
delete from incStatement;    
delete from sqlite_sequence where name='incStatement';
delete from info;    
delete from sqlite_sequence where name='info';
delete from overall;    
delete from sqlite_sequence where name='overall';
delete from mission;    
delete from sqlite_sequence where name='mission';
"""
