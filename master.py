##import mysql.connector
import getpass
import pymysql

##Connect to DB
uname = 'nuinstig_goat'
pword = 'kzzgBq_o]uVF'
ip = '162.241.217.12'
hostn = "box5445.bluehost.com"
while True:
    try:
        cnx = pymysql.connect(host=ip,user=uname, password=pword,db='nuinstig_goats',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        break

    except pymysql.err.OperationalError as error:
        print(error)
        break
    
cur = cnx.cursor()



            
                            
