#!/usr/bin/python

#THIS FORK OF THE SCANNER APPLICATION IS FOR USE ON RESTRICTED ACCESS APPLICATIONS WHERE USERS ARE NOT PERMITED TO
#ENTER AN AREA TWICE, DO NOT USE FOR STANDARD CHECK-IN

import MySQLdb as mdb
import sys
import curses
import commands
curwindow = curses.initscr()

def curses_startup():
	curwindow.border(0)
	curses.start_color()
	curses.noecho()
	curses.curs_set(0)
	curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_GREEN, curses.COLOR_BLACK)
	curwindow.addstr(1,23, "Checkpoint version 0.3.2 alpha", curses.color_pair(1))
	curwindow.addstr(13,35, "READY", curses.color_pair(1))
	curwindow.keypad(1)
	curwindow.refresh()

def draw_border_info():
	curwindow.clear()
	curwindow.border(0)
	curwindow.addstr(1,23, "Checkpoint version 0.2.1 alpha", curses.color_pair(1))
	curwindow.refresh()
	
def stripdata(cardnumber):	#ONLY NEEDED FOR MAGNETIC CARDS, NOT FOR BARCODES
	card_id=cardnumber.lstrip('%B')     #Remove the sentinel for track one
	card_id_list=card_id.split('^')  #Split the track using the "^" sentinel so we can pull the card id easily  
	card_id=card_id_list[0]          #We now have just the card id
	return card_id

def codetype(code):
	if(code is 9780801993077):importdata()
	if(code is 9780745612959):exportdata()

def mountdrives():
	volname=commands.getstatusoutput('ls /dev/disk/by-label')
	pointstring="ls -al /dev/disk/by-label | grep {0}".format(volname[1])
	mountpointtuple=commands.getstatusoutput(pointstring)
	mountpoint=str(mountpointtuple[1])
	mountpointlst=mountpoint.split(" ")
	mountpoint=mountpointlst[12]
	mountpoint=mountpoint.lstrip("../")
	mountstring="sudo mount /dev/{0} /media/usb".format(mountpoint)

#def importdata():

#def exportdata():

con = None
colorstatus=0
curses_startup() #Set up our curses interface
while 1 is 1:
	try:
		# promethus -> prometheus
		con = mdb.connect('localhost','pi','','scanner'); #Not final sql details
		cur = con.cursor()
		#card_id = raw_input("====> ")   #NO LONGER USED 
		card_id=curwindow.getstr()
		draw_border_info()
		locationid=00
		cur.execute("use scanner") #Make sure we're in the right table
		idcheck="SELECT * FROM scanner WHERE card_id = {0}".format(card_id) #Prepare check statment
		cur.execute(idcheck)
		checkresult=cur.fetchone()
		if checkresult is None:
			sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'ACCEPTED', {1});".format(card_id,locationid) #Punch the user in
			status="Accepted"
			colorstatus=3
		elif checkresult is not None:
			sqlstring="INSERT INTO scanner (card_id, punch_in_or_out,location_code) VALUES({0}, 'REJECTED', {1});".format(card_id,locationid) #Punch the user out
			status="Not Accepted"
			colorstatus=2
		screen_text="User: {0} scan {1}".format(card_id,status)
		curwindow.addstr(14,27,screen_text,curses.color_pair(colorstatus))
		curwindow.refresh()
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
