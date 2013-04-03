#!/usr/bin/python

import MySQLdb as mysql
import sys
import commands
import socket

# define static global vars and sockets
location_id = socket.gethostname()
mysql_connection = None

import_magic = 9780801993077
export_magic = 9780745612959

# panic(string error_string, int error_code)
# print exception and kill the script
def panic(error_string, error_code):
    string = "[!] {0}: {1}".format(error_code, error_string)
    print(string)
    sys.exit(error_code)

def barcode_input(code):
    # switch statement in python?
    if (int(code) == import_magic):
        import_data()
    if (int(code) == export_magic):
        export_data()

# mount the thumb drive connected to the raspberry pi
def mount_drives():
    mount_grep  = "ls -lA /dev/disk/by-label/ | perl -i -p -e 's/\n//' | sed -e 's/.*\///g'"
    mount_point = commands.getstatusoutput(mount_grep)
    mount_cmd   = "sudo mount -t vfat /dev/{0} /media/usb".format(str(mount_point[1]))
    mount_ret   = commands.getstatusoutput(mount_cmd)

def umount_drives():
    unmount_ret = commands.getstatusoutput("sudo umount /media/usb")
    
def import_data():
    mount_drives()
    import_string = "sudo mysql -h localhost -u root scanner < /media/usb/auth_id"
    dump_result   = commands.getstatusoutput(import_string)
    umount_drives()

def export_data():
    mount_drives()
    dump_string = "sudo mysqldump -h localhost -u root scanner > /media/usb/{0}.sql".format(location_id)
    dump_result = commands.getstatusoutput(dump_string)
    umount_drives()

def mysql_connect(hostname, username, password, database):
    return mysql.connect(hostname, username, password, database)

while 1 is 1:
    try:
        # initialize mysql connection
        # possibly move outside of loop?
        mysql_connection = mysql_connect('localhost', 'root', '', 'scanner')
        mysql_cursor = mysql_connection.cursor()
        mysql_cursor.execute("use scanner")

        # grab input from terminal
        card_id = input('> ')
        barcode_input(card_id)
        card_id = curwindow.getstr()

        # table layout /
        #   scan (id, barcode, location, [time])

        # time = date()
        # no longer need to verify scan
        # check for duplicate scans'

        # input scan data into table
        sqlstring = "INSERT INTO scan (barcode, location, time) VALUES({0}, {1}, {2});".format(card_id, location_id, time)
        mysql_cursor.execute(sqlstring)
        mysql_connection.commit()

    except mysql.Error, error:
        mysql_connection.rollback()
        panic(error, 1)

    finally:
        if mysql_connection:
            mysql_connection.close()
