#!/usr/bin/python

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

import MySQLdb as mdb
import sys
import curses
import commands

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

def codetype(code):
    if (code is 9780801993077):
        importdata()
    if (code is 9780745612959):
        exportdata()

# Mounts the thumb drive connected to the raspberry pi for
# database extraction
def mountdrives():
    volname = commands.getstatusoutput('ls /dev/disk/by-label')
    pointstring = "ls -al /dev/disk/by-label | grep {0}".format(volname[1])
    mountpointtuple = commands.getstatusoutput(pointstring)
    mountpoint = str(mountpointtuple[1])
    mountpointlst = mountpoint.split(" ")
    mountpoint = mountpointlst[12]
    mountpoint = mountpoint.lstrip("../")
    mountstring = "sudo mount /dev/{0} /media/usb".format(mountpoint)

#def importdata():

#def exportdata():

def mysql_connect(hostname, username, password, database):
    return mdb.connect(hostname, username, password, database)

"""
    todo:
        - define functions for separate mysql processes
"""

# Define static global vars
location_id = socket.gethostname()
mysql_connection = mysql_connect('localhost', 'pi', '', 'scanner')
mysql_cursor = mysql_connection.cursor()
mysql_cursor.execute("use scanner")

curses_startup()
status_color = 0

while 1 is 1:
    # [~~] I don't believe that we need to have exception handling
    #      over the entire process, it should be divided into subroutines

    try:
        card_id = curwindow.getstr()
        draw_border_info()
        idcheck = "SELECT * FROM scanner WHERE card_id = {0}".format(card_id)
        cur.execute(idcheck)
        checkresult = cur.fetchone()

        if checkresult is None:
            sqlstring = "INSERT INTO scanner (card_id, punch_in_or_out, location_code) VALUES({0}, 'ACCEPTED', {1});".format(card_id, locationid)
            status = "Accepted"
            status_color = 3

        elif checkresult is not None:
            sqlstring = "INSERT INTO scanner (card_id, punch_in_or_out, location_code) VALUES({0}, 'REJECTED', {1});".format(card_id, locationid)
            status = "Not Accepted"
            status_color = 2
            screen_text = "User: {0} scan {1}".format(card_id,status)
            curwindow.addstr(14, 27, screen_text, curses.color_pair(status_color))
            curwindow.refresh()
            cur.execute(sqlstring)
            mysql_connection.commit()

    except mdb.Error, e:
        curses.endwin()
        mysql_connection.rollback()
        panic(e, 1)

    finally:
        if mysql_connection:
            mysql_connection.close()
            curses.endwin()
