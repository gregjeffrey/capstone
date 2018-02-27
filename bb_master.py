import getpass, pymysql, time
import Adafruit_BBIO.PWM as PWM
from serial import Serial

## Database Setup
##Connect to DB
def db_init():
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

	return cnx
	
#Adds collected data to the database	
def add_measurements(cnx,cur,data,img):
    #data format for SQL datetime: YYYY-MM-DD hh:mm:ss
	
	vals = list(data.values())
	vals.append(img)
    #List should look like this: [t,loc_no,insects,ndvi,water,chlora,chlorb,img]
    cur.callproc('add_measurements', values)
    cnx.commit

	
## Motor Control
def move_motor(location):
	PWM.start('P9_14',duty)
	
	
def collect_data(usb_cnx,img_size):
	#Send a command to the Pyboard via USB to take a photo & run algorithms
	#Pyboard should be listening for a 1 from the BB
	prt.write(1)
	
	#Listen for response from Pyboard
	t = time.time()
	data = prt.read(datasize) #Collect other data - will come first
	img = prt.read(img_size) #Collect image data - will come second
	
	#Process the byte arrays into usable data
	##
	##
	
	data_dict = {'t':t,'location_no':loc_no,'insects':insects,'ndvi':ndvi,'water':water,'chlora':chlora,'chlorb',chlorb}
	
	return (data_dict,img)
	
	
## Main Loop
def main():
	
	#Set image size
	img_size = 5000
	datasize = 100
	
	#Initialize database
	cnx = db_init()
	cur = cnx.cursor()
	
	## Setup Serial connection with USB
	##BB defaults to ttyACM0, but sometimes uses ttyACM1 if PyBoard is reset or hot-plugged
	try:
		prt = Serial(port='/dev/ttyACM0',baudrate=9600,timeout=None)
	except:
		prt = Serial(port='/dev/ttyACM1',baudrate=9600,timeout=None)
	
	location = 1
	
	while(1):
	
		#Move motor to desired location
		move_motor(location)
		
		#Tell PyBoard to take a photo, run algorithms, send data back to BB over USB
		(data,img) = collect_data(usb_cnx,img_size,datasize)
		
		#Send the data to the database
		add_measurements(cnx,cur,data,img)
		
		if location == 9:
			location = 1
		else:
			location += 1
		
		#Rinse and repeat
	
	
	
		
			
	






	
