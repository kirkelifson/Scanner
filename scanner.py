#!/usr/bin/python

import MySQLdb as mdb
import sys
import random as random
con = None

try:
        con = mdb.connect('localhost','scanner_test','promethus','scanner'); #Not final sql details
        cur = con.cursor()
        id_count=19
        card_ids=[1286273112610971601,6697362592043932053,3432959665415480118,3398201920219742397,8186775750190939895,7881344916677369314,1534863508379365074,6697362592043932053,2138569275305770607,3432959665415480118,3398201920219742397,4758873730368976908,1286273112610971601,1534863508379365074,8186775750190939895,2138569275305770607,2128516085003048783,4758873730368976908,7881344916677369314]
        #cardid=random.randint(1000000000000000000,9000000000000000000) #Create a random card id, but we use an array to test both in and out now
        for x in range(len(card_ids)):
                card_id=card_ids[x]
                locationid=random.randint(1,99) #Create a random location code
                cur.execute("use scanner") #Make sure we're in the right table
                idcheck="SELECT * FROM scanner WHERE card_id = {0}".format(card_id) #Prepare check statment
                cur.execute(idcheck)
                checkresult=cur.fetchone()
                #print(checkresult)     Unneeded debug statment
                if checkresult is None:
                        sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'IN', {1});".format(card_id,locationid) #Punch the user in
                elif checkresult is not None:
                        sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'OUT', {1});".format(card_id,locationid) #Punch the user out

                #print(checkresult)     DEBUG STATMENTS
                #print(sqlstring)       DEBUG STATMENTS
                cur.execute(sqlstring) #Execute the actual SQL transaction
                con.commit() #Commit the change to the db

except mdb.Error, e:
        con.rollback() #Something went really wrong
        print "error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

finally:
        if con:
                con.close()

