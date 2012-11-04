#!/usr/bin/python

import MySQLdb as mdb
import sys
import curses
import random as random
curwindow = curses.initscr()

def curses_startup():
	curwindow.border(0)
	curses.start_color()
	curses.noecho()
	curses.curs_set(0)
	curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLACK)
	curwindow.addstr(1,23, "Checkpoint version 0.1.1 alpha", curses.color_pair(1))
	curwindow.addstr(14,27, "Waiting for card....", curses.color_pair(1))
	curwindow.keypad(1)
	curwindow.refresh()

def draw_border_info():
	curwindow.clear()
	curwindow.border(0)
	curwindow.addstr(1,23, "Checkpoint version 0.1.1 alpha", curses.color_pair(1))
	curwindow.refresh()
	
def importdb():		#Import the new card database (users)

def exportdb():		#Export the current card database (punches)

def id_card_type(cardid):	#Check card type
	sqlstring="select type from admincards where card = {0}".format(cardid)
	idtype=cur.fetchone()
	if idtype is "export":
		return("export")
	else if idtype is "import":
		reutrn("import")
	else:
		return("normal")

	
run=1
color=0
con = None
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
		idtype=id_card_type(card_id)	 #Check card type, prepare to import or export the card database
		if idtype is "export":
			exportdb()
		else if idtype is "import":
			importdb()
		draw_border_info()
		locationid=0	#0 relates to the testing device
		cur.execute("use scanner") #Make sure we're in the right table
		idcheck="SELECT * FROM scanner WHERE card_id = {0}".format(card_id) #Prepare check statment
		cur.execute(idcheck)
		checkresult=cur.fetchone()
		if checkresult is None:
			sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'IN', {1});".format(card_id,locationid) #Punch the user in
			status="Accepted"
			color=2
		elif checkresult is not None:
			sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'OUT', {1});".format(card_id,locationid) #Punch the user out
			status="Not Accepted"
			color=3
		screen_text="User: {0} scan {1}".format(card_id,status)
		curwindow.addstr(14,27,screen_text,curses.color_pair(color))
		draw_border_info()
		cur.execute(sqlstring) #Execute the actual SQL transaction
		con.commit() #Commit the change to the db

	except mdb.Error, e:
		curses.endwin()
		con.rollback() #Something went really wrong
		print "error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:
  		if con:
			con.close()
			curses.endwin()
