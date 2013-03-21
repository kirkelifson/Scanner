#!/usr/bin/python

import MySQLdb as mdb
import sys
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
# Define static global vars and sockets
location_id = socket.gethostname()
mysql_connection = None

import_magic = 9780801993077
export_magic = 9780745612959


# panic(string error_string, int error_code)
# Exits the program and displays the error code that was thrown along with a description
def panic(error_string, error_code):
    string = "[!!] {0}: {1}".format(error_code, error_string)
    print(string)
    sys.exit(error_code)

# Initializes ncurses and displays version information on startup
def codetype(code):
    if (int(code) == import_magic):
       importdata()
    if (int(code) == export_magic):

def isspecial(code):
    if(int(code) == import_magic or int(code) == export_magic):
        return 1

# Mounts the thumb drive connected to the raspberry pi for
# database extraction
def mountdrives():
    mountpointstring = "ls -lA /dev/disk/by-label/ | perl -i -p -e 's/\n//' | sed -e 's/.*\///g'"
    mountpoint = commands.getstatusoutput(mountpointstring)
    mountingstring = "sudo mount -t vfat /dev/{0} /media/usb".format(str(mountpoint[1]))
    outputstatus = commands.getstatusoutput(mountingstring)

def unmountdrives():
    unmountresult = commands.getstatusoutput("sudo umount /media/usb")
    
def importdata():
    mountdrives()
    import_string = "sudo mysql -h localhost -u root scanner < /media/usb/auth_id"
    dumpresult = commands.getstatusoutput(import_string)
    unmountdrives()
    return 0

def exportdata():
    mountdrives()
    dump_string = "sudo mysqldump -h localhost -u root scanner > /media/usb/{0}.sql".format(location_id)
    dumpresult = commands.getstatusoutput(dump_string)
    unmountdrives()
    return 0

def mysql_connect(hostname, username, password, database):
    return mdb.connect(hostname, username, password, database)

while 1 is 1:
    try:
        mysql_connection = mysql_connect('localhost', 'root', '', 'scanner')
        mysql_cursor = mysql_connection.cursor()
        mysql_cursor.execute("use scanner")
        card_id = input('>')    
        if(isspecial(card_id) == 1):    
            codetype(card_id)
            card_id = curwindow.getstr()
        idcheck = "SELECT * FROM scan_data WHERE card_id = {0}".format(card_id)
        mysql_cursor.execute(idcheck)
        checkresult = mysql_cursor.fetchone()
        if checkresult is None:
            sqlstring = "INSERT INTO scan_data (card_id, scan_type, location_code) VALUES({0}, 'ACCEPTED', {1});".format(card_id, location_id)
        elif checkresult is not None:
            if(seconds_status == 0):
                sqlstring = "INSERT INTO scan_data (card_id, scan_type, location_code) VALUES({0}, 'REJECTED', {1});".format(card_id, location_id)
            else:
                sqlstring = "INSERT INTO scan_data (card_id, scan_type, location_code, seconds) VALUES({0}, 'ACCEPTED', {1}, 1);".format(card_id, location_id)
        mysql_cursor.execute(sqlstring)
        mysql_connection.commit()

    except mdb.Error, e:
        curses.endwin()
        mysql_connection.rollback()
        panic(e, 1)

    finally:
        if mysql_connection:
            mysql_connection.close()
            curses.endwin()
