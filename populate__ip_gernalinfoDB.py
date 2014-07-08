#!/usr/bin/python

import sqlite3
import sys
import re

fo = open(sys.argv[1])
inF = fo.read()

def getFieldValue (filedName):
	regex = re.compile(filedName+':(.*)')
	try:
		return regex.search(inF).groups()[0]
	except:
		return None

MinistryName = getFieldValue('MinistryName')
OrganizationName = getFieldValue('OrganizationName')
YearFounded = getFieldValue('YearFounded')
HQAddress = getFieldValue('HQAddress')
State = getFieldValue('State')
City = getFieldValue('City')
ZipCode = getFieldValue('ZipCode')
Country = getFieldValue('Country')
Website = getFieldValue('Website')
Phone = getFieldValue('Phone')
Fax = getFieldValue('Fax')
PrimaryContactTitle = getFieldValue('PrimaryContactTitle')
PrimaryContactPhone = getFieldValue('PrimaryContactPhone')
PrimaryContactEmail = getFieldValue('PrimaryContactEmail')
TaxID = getFieldValue('TaxID')
MinitryType = getFieldValue('MinitryType')
CEONameTitle = getFieldValue('CEONameTitle')
ProgramTargetPopulation = getFieldValue('ProgramTargetPopulation')
PartnerOrganizations = getFieldValue('PartnerOrganizations')
NonprofitPeers = getFieldValue('NonprofitPeers')
OtherProgramAreas = getFieldValue('OtherProgramAreas')

valArry = [None, MinistryName, OrganizationName, YearFounded, HQAddress,
			State, City, ZipCode, Country,
			Website, Phone, Fax, PrimaryContactTitle, PrimaryContactPhone,
			PrimaryContactEmail, TaxID, MinitryType, CEONameTitle,
			ProgramTargetPopulation, PartnerOrganizations, NonprofitPeers, OtherProgramAreas]

conn = sqlite3.connect('ip_generalInfo.db')

cursor = conn.cursor()

sql = '''INSERT INTO info VALUES (
			?,?,?,?,	
			?,?,?,?,
			?,?,?,?,
			?,?,?,?,
			?,?,?,?,
			?,?)'''

cursor.execute(sql, valArry)

conn.commit()
conn.close()
