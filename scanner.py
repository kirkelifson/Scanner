#!/usr/bin/python

import MySQLdb as mysql
import sys
import commands
import socket
import time

# define static global vars and sockets
location_id = socket.gethostname()
mysql_connection = None

import_magic   = 9780801993077
export_magic   = 9780745612959
location_magic = 9781027298277

# panic(string error_string, int error_code)
# print exception and kill the script
def panic(error_string, error_code):
    string = "[!] {0}: {1}".format(error_code, error_string)
    print(string)
    sys.exit(error_code)

def barcode_input(code):
    if   (int(code) == import_magic):
        import_data()
        return 1
    elif (int(code) == export_magic):
        export_data()
        return 1
    elif (int(code) == location_magic):
        change_location()
        return 1

    return 0

# mount the thumb drive connected to the raspberry pi
def mount_drive():
    mount_grep  = "ls -lA /dev/disk/by-label/ | perl -i -p -e 's/\n//' | sed -e 's/.*\///g'"
    mount_point = commands.getstatusoutput(mount_grep)
    mount_cmd   = "sudo mount -t vfat /dev/{0} /media/usb".format(str(mount_point[1]))
    mount_ret   = commands.getstatusoutput(mount_cmd)

def umount_drive():
    unmount_ret = commands.getstatusoutput("sudo umount /media/usb")
    
def import_data():
    mount_drive()
    import_string = "sudo mysql -h localhost -u root scanner < /media/usb/auth_id"
    import_result = commands.getstatusoutput(import_string)
    umount_drive()

def export_data():
    mount_drive()
    dump_string = "sudo mysqldump -h localhost -u root scanner > /media/usb/{0}.sql".format(location_id)
    dump_result = commands.getstatusoutput(dump_string)
    umount_drive()

def change_location():
    new_location = input('(new location)> ')
    hostname_file = open("/etc/hostname", "w")
    hostname_file.write(new_location);
    hostname_file.close()

def mysql_connect(hostname, username, password, database):
    return mysql.connect(hostname, username, password, database)

# connect to mysql database
mysql_connection = mysql_connect('localhost', 'root', '', 'scanner')
mysql_cursor = mysql_connection.cursor()
mysql_cursor.execute("use scanner")

while 1 is 1:
    try:
        # grab input from terminal
        card_id = input('> ')
        special = barcode_input(card_id)
        time = time.time()

        # table layout /
        #   scans (id, barcode, location, [time])

        # check for duplicate scans
        # time difference between last scan?
        # if < 5 sec && same code, deny

        # input scan data into table
        sqlstring = "INSERT INTO scans (barcode, location, time, special) VALUES({0}, '{1}', {2});".format(card_id, location_id, time, special)
        mysql_cursor.execute(sqlstring)
        mysql_connection.commit()

    except mysql.Error, error:
        mysql_connection.rollback()
        panic(error, 1)

    finally:
        if mysql_connection:
            mysql_connection.close()
