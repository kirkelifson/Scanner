#!/usr/bin/python

import MySQLdb as mdb
import sys
import curses
import random as random

def curses_startup():
	curwindow = curses.initscr()
	curwindow.border()
	curses.start_color()
	curses.noecho()
	curses.curs_set(0)
	curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
	curwindow.addstr(1,23, "Checkpoint version 0.1.1 alpha", curses.color_pair(1))
	curwindow.addstr(12,23, "Waiting for card....", curses.color_pair(1))

def draw_border_info():
	curwindow.border()
	curwindow.addstr(1,23, "Checkpoint version 0.1.1 alpha", curses.color_pair(1))
	
	
con = None
run=1
curses_startup() #Set up our curses interface
while run is 1:
	try:
		# promethus -> prometheus
		con = mdb.connect('localhost','pi','','scanner'); #Not final sql details
		cur = con.cursor()
		#card_id = raw_input("====> ")   #NO LONGER USED 
		card_id=curwindow.getstr()
		card_id=card_id.lstrip('%B')     #Remove the sentinel for track one
		card_id_list=card_id.split('^')  #Split the track using the "^" sentinel so we can pull the card id easily  
		card_id=card_id_list[0]          #We now have just the card id
		curwindow.erase()
		draw_border_info()
		locationid=random.randint(1,99) #Create a random location code
		cur.execute("use scanner") #Make sure we're in the right table
		idcheck="SELECT * FROM scanner WHERE card_id = {0}".format(card_id) #Prepare check statment
		cur.execute(idcheck)
		checkresult=cur.fetchone()
		if checkresult is None:
			sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'IN', {1});".format(card_id,locationid) #Punch the user in
			status="Accepted"
		elif checkresult is not None:
			sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'OUT', {1});".format(card_id,locationid) #Punch the user out
			status="Not Accepted"
		curwindow.addstr(12,23,"User: {0} scan {1}".format(card_id,status),curses.color_pair(1))
		curwindow.refresh()
		cur.execute(sqlstring) #Execute the actual SQL transaction
		con.commit() #Commit the change to the db

	except mdb.Error, e:
		con.rollback() #Something went really wrong
		print "error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
  		if con:
    			con.close()
				


