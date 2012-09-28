#!/usr/bin/python

import MySQLdb as mdb
import sys
import random as random
con = None

try:
	con = mdb.connect('localhost','scanner_test','promethus','scanner'); #Not final sql details
	cur = con.cursor()
	cardid=random.randint(1000000000000000000,9000000000000000000) #Create a random card id
	locationid=random.randint(1,99) #Create a random location id
	cur.execute("use scanner") #Make sure we're in the right table
	idcheck="SELECT * FROM scanner WHERE card_id = {0}".format(cardid) #Prepare check statment			
	cur.execute(idcheck)
	checkresult=cur.fetchone()
	#print(checkresult)	#DEBUG STATMENTS
	if checkresult is None:
		sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'IN', {1});".format(cardid,locationid) #Punch the user in
	elif checkresult is not None:
		sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'OUT', {1});".format(cardid,locationid) #Punch the user out
	
	#print(checkresult)	DEBUG STATMENTS
	#print(sqlstring)	DEBUG STATMENTS
	cur.execute(sqlstring) #Execute the actual SQL transaction
	con.commit() #Commit the change to the db

except mdb.Error, e:
	con.rollback() #Something went really wrong
	print "error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)

finally:
	if con:
		con.close()

	
