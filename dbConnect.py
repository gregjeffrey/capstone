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

hostname="162.241.217.12"
username="nuinstig_goat"
password="kzzgBq_o]uVF"
database="nuinstig_goats"
charset = "utf8mb4"
cursorType = pymysql.cursors.DictCursor

def connect():
    return pymysql.connect(host=hostname,
                         user=username,
                         password=password,
                         db=database,
                         charset=charset,
                         cursorclass=cursorType)

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
