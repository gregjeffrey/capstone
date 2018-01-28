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


def add_measurements(t,loc_no,insects,ndvi,water,chlora,chlorb):
    #data format for SQL datetime: YYYY-MM-DD hh:mm:ss
    values = [t,loc_no,insects,ndvi,water,chlora,chlorb]
    cur.callproc('add_measurements', values)
    cnx.commit

t = "2018-01-28 14:30:00"
loc_no = 1
insects = True
ndvi = 2
water = 3
chlora = 4
chlorb = 5

add_measurements(t,loc_no,insects,ndvi,water,chlora,chlorb)

stmt = 'SELECT * FROM measurements'
cur.execute(stmt)
cnx.fetchall()

    
    




            
                            
