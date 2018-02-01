#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Matt
#
# Created:     29/01/2018
# Copyright:   (c) Matt 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pymysql

def connect(hostname, username, password, database, charset, cursorType):
    db = pymysql.connect(host=hostname,    # your host, usually localhost
                         user=username,         # your username
                         password=password,  # your password
                         db=database,
                         charset=charset,
                         cursorclass=cursorType)

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    return cur
