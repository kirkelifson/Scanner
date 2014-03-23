#!/usr/bin/python
# table layout: scans (id, barcode, location, timestamp)

import sqlite3 as sql
import sys
import os
import commands
import socket
import time

# define static global vars and sockets
location_id = socket.gethostname()
sql_connection = sql.connect(location_id + '.db')
sql_cursor     = sql_connection.cursor()
sql_cursor.execute('create table if not exists scans(id integer primary key, barcode text, location text, timestamp integer);')

magic = {
        'import'  : 9780801993000,
        'export'  : 9780801993001,
        # place next in 02 pos, then 05
        'empty'   : 9780801993003,
        'shutdown': 9780801993004
        }

# panic(string error_string, int error_code)
# print exception and kill the script
def panic(error_string, error_code):
    sql_connection.rollback()
    string = "[!] {0}: {1}".format(error_code, error_string)
    print(string)
    sys.exit(error_code)

def flag(code):
    if   (code == magic['import']):
        import_data()
    elif (code == magic['export']):
        export_data()
    elif (code == magic['empty']):
        empty_db()
    elif (code == magic['shutdown']):
        shutdown()

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
    import_string = "sudo sql -u root scanner < /media/usb/auth_id"
    import_result = commands.getstatusoutput(import_string)
    umount_drive()

def export_data():
    mount_drive()
    dump_string = "sudo sqldump -u root scanner > /media/usb/{0}.sql".format(location_id)
    dump_result = commands.getstatusoutput(dump_string)
    umount_drive()

def shutdown():
    umount_drive()
    sql_connection.close()
    os.system("sudo poweroff")

def empty_db():
    try:
        sql_cursor.execute("truncate scans")

    except sql.Error, error:
        panic(error, 1)

while 1:
    try:
        barcode = input('> ')

        # catch magic numbers
        if int(barcode) in magic.values():
            flag(int(barcode))

        else:
            unix_timestamp = time.time()
            query = "INSERT INTO scans (barcode, location, timestamp) VALUES({0}, '{1}', {2});".format(barcode, location_id, unix_timestamp)
            sql_cursor.execute(query)
            sql_connection.commit()

    except sql.Error, error:
        panic(error, 1)
