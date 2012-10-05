#!/usr/bin/python

import MySQLdb as mdb
import sys
import random as random
con = None

try:
  # promethus -> prometheus
  con = mdb.connect('localhost','pi','','scanner'); #Not final sql details
  cur = con.cursor()
  card_id = raw_input("====> ")
  card_id=card_id.lstrip('%B')
  card_id_list=card_id.split('^')
  card_id=card_id_list[0]
  print(card_id)
  locationid=random.randint(1,99) #Create a random location code
  cur.execute("use scanner") #Make sure we're in the right table
  idcheck="SELECT * FROM scanner WHERE card_id = {0}".format(card_id) #Prepare check statment
  cur.execute(idcheck)
  checkresult=cur.fetchone()
  if checkresult is None:
    sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'IN', {1});".format(card_id,locationid) #Punch the user in
  elif checkresult is not None:
    sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'OUT', {1});".format(card_id,locationid) #Punch the user out
  cur.execute(sqlstring) #Execute the actual SQL transaction
  con.commit() #Commit the change to the db

except mdb.Error, e:
  con.rollback() #Something went really wrong
  print "error %d: %s" % (e.args[0],e.args[1])
  sys.exit(1)

finally:
  if con:
    con.close()
