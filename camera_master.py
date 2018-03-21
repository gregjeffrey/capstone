import sensor, image, time, pyb,ustruct


#Sends a message in three stages:
#Stage 1: length of the message's format string as a 4-byte int
#Stage 2: the message's format string as a str
#Stage 3: the message itself as a tuple
#Assumes msg is a tuple of the form (x1,x2,...,xn) with any strings encoded as bytes and no "nested" tuples
#EVEN IF YOU ARE JUST SENDING ONE STRING, PUT IT IN A TUPLE BY ITSELF
#fmtstr is a str
#Condition data as such before calling the function
def send_msg(fmtstr,msg,port):
	try:
		#Stage 1: Length of message's format string
		fmtstrsize = len(fmtstr)
		stg1_msg = ustruct.pack('@i',fmtstrsize)
		
		stg2_fmtstr = '@%is' % (fmtstrsize) # Format-stringception
		stg2_msg = ustruct.pack(stg2_fmtstr,fmtstr.encode()) #Stage 2: Send The message's format string
		
		stg3_msg = ustruct.pack(fmtstr,*msg) #Stage 3: The data tuple
		
		#Write the message(s) to the port
		port.write(stg1_msg)
		port.write(stg2_msg)
		port.write(stg3_msg)
		
		return 1
	except:
		return -1
	
def recv_msg(port):
	#Best way to read a line from the USB_VCP
	
	def getln():
		while(1):
			if port.any():
				msg = port.readline()
				break
		return msg #Returns raw bytes message
		
	try:
		stg1 = getln()
		fmtstr_size = ustruct.unpack('@3s',stg1)[0] # Receive stage 1- the size of the format string
		fmtstr_size = int(fmtstr_size.decode()) #Turns it back into an actual fucking number

		fmtstringception = '@%is' % fmtstr_size # The format string of the format string = fmtstringception
		#Receive stage 2 - the format string
		stg2 = getln()
		fmtstr = ustruct.unpack(fmtstringception,stg2)[0]
		fmtstr = fmtstr.decode()
		
		#Receive stage 3 - the Data
		stg3 = getln()
		data = ustruct.unpack(fmtstr,stg3)
				
		return data
		
	except:
		return -1

	
def send_img(img,port):
	try:
		jpg = img.compressed() # Creates jpg byte object
		sz = jpg.size()
		packed_size = ustruct.pack('@i',sz)
		port.write(packed_size)
		port.send(jpg)
		return 1
	except:
		return -1
	
	
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

brd = pyb.USB_VCP()
brd.setinterrupt(-1)

led1 = pyb.LED(1)
led2 = pyb.LED(2)

triggerstring = 'Go'

while(1):
	if brd.isconnected(): # Listen for the command/trigger
		
		#Does a few flashes if the USB is connected
		for i in range(3):
			led2.on()
			time.sleep(500)
			led2.off()
		
		
		cmd = recv_msg(brd)[0].decode() # Looks for initialization command
		if cmd == triggerstring:
			led1.on()
			
			avg_data = recv_msg(brd) #Receive calibration data/moving averages from BB
			if avg_data != -1:
				led2.on()
			
			##############################################
			### Camera People - Do all your shit here! ###
			##############################################
			
			img = sensor.snapshot()
			
			#Format data to be sent back to the Beaglebone
			#see send_msg() function for description
			#As long as it is formatted as such, BB can handle it (I promise) (i hope...)
			msg = (1,b'Nick Sucks',2,b'Calvin Sucks Too')
			fmtstr = '@i10si16s'
			
			#Send the image
			success = send_msg(fmtstr,msg,brd)
			imgsuccess = send_img(img,brd)
			time.sleep(1000)
			
			led1.off()
			led2.off()
		
		

		
                                        
				
	
	

