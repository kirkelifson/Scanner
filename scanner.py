#!/usr/bin/python

import MySQLdb as mdb
import sys
import curses
import commands
import socket

"""
Description:

scanner.py runs on an individual Raspberry Pi station which is designed
to read barcodes from ID badges. Once the code is scanned the attendee
will be cross-checked with the database to verify that he or she has
not been previously checked in. This program will assist in keeping track
of attendees at Order of the Arrow events for Seminole Lodge 85.

Version: 0.2 [02/03/13]

"""

import_magic = 9780801993077
export_magic = 9780745612959

curwindow = curses.initscr()

# panic(string error_string, int error_code)
# Exits the program and displays the error code that was thrown along with a description
def panic(error_string, error_code):
    print "[!!] %d: %s\n" % (error_code, error_string)
    sys.exit(error_code)

# Initializes ncurses and displays version information on startup
def curses_startup():
    curwindow.border(0)
    curses.start_color()
    curses.noecho()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curwindow.addstr(1, 23, "Checkpoint version 0.2", curses.color_pair(1))
    curwindow.addstr(13, 35, "READY", curses.color_pair(1))
    curwindow.keypad(1)
    curwindow.refresh()

def draw_border_info():
    curwindow.clear()
    curwindow.border(0)
    curwindow.addstr(1, 23, "Checkpoint version 0.2", curses.color_pair(1))
    curwindow.refresh()

# [^^] possibly merge into a larger function when reading in the data?
def codetype(code):
    if (int(code) == import_magic):
       importdata()
    if (int(code) == export_magic):
        exportdata()

def isspecial(code):
    if(int(code) == import_magic or int(code) == export_magic):
        return 1

# Mounts the thumb drive connected to the raspberry pi for
# database extraction
def mountdrives():
    mountpointstring= "ls -lA /dev/disk/by-label/ | perl -i -p -e 's/\n//' | sed -e 's/.*\///g"
    mountpoint=commands.getstatusoutput(mountpointstring)
    mountingstring="sudo mount -t vfat {0} /media/usb".format(str(mountpoint[0]))
    outputstatus=commands.getstatusoutput(mountingstring)

def unmountdrives():
    unmountresult=commands.getstatusoutput("umount /media/usb")
    
def importdata():
    return 0



def exportdata():
    mountdrives()
    draw_border_info()
    curses.addstr(13,35,"DRIVES MOUNTED DO NOT REMOVE", curses.color_pair(2))
    curses.addstr(13,36,"EXPORTING SCAN DATA", curses.color_pair(2))
    curwindow.refresh()
    dumpresult=commands.getstatusoutput("mysqldump -h localhost -u root >/media/usb/sqldump")
    draw_border_info()
    unmountdrives()
    curwindow.addstr(13,35,"DRIVES UNMOUNTED", curses.color_pair(2))
    curwindow.addstr(13,36,"RESUMING NORMAL OPERATION", curses.color_pair(2))
    curwindow.refresh()

def mysql_connect(hostname, username, password, database):
    return mdb.connect(hostname, username, password, database)

"""
    todo:
        - define functions for separate mysql processes
"""

# Define static global vars and sockets
#location_id = socket.gethostname()
location_id=00
mysql_connection=None
curses_startup()
status_color = 0

while 1 is 1:
    # [~~] I don't believe that we need to have exception handling
    #      over the entire process, it should be divided into subroutines

    try:
        mysql_connection = mysql_connect('localhost', 'root', '', 'scanner')
	mysql_cursor = mysql_connection.cursor()
	mysql_cursor.execute("use scanner")
        card_id = curwindow.getstr()
        if(isspecial(card_id) is 1):    
            codetype(card_id)
            card_id = curwindow.getstr()
        draw_border_info()
	# [^^] move idcheck into a separate subroutine
        idcheck = "SELECT * FROM scan_data WHERE card_id = {0}".format(card_id)
        mysql_cursor.execute(idcheck)
        checkresult = mysql_cursor.fetchone()
        if checkresult is None:
            sqlstring = "INSERT INTO scan_data (card_id, scan_type, location_code) VALUES({0}, 'ACCEPTED', {1});".format(card_id, location_id)
            status = "Accepted"
            status_color =3 
        elif checkresult is not None:
            sqlstring = "INSERT INTO scan_data (card_id, scan_type, location_code) VALUES({0}, 'REJECTED', {1});".format(card_id, location_id)
            status = "Not Accepted"
            status_color = 2
	screen_text = "User: {0} scan {1}".format(card_id,status)
        curwindow.addstr(14, 27, screen_text, curses.color_pair(status_color))
        curwindow.refresh()
        mysql_cursor.execute(sqlstring)
        mysql_connection.commit()

    except mdb.Error, e:
        curses.endwin()
        mysql_connection.rollback()
        panic(e, 1)

    finally:
        # [~~] how would we not have a mysql connection?
        if mysql_connection:
            mysql_connection.close()
            curses.endwin()
