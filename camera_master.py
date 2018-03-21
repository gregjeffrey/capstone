import sensor, image, time, pyb,ustruct


#Sends a message in three stages:
#Stage 1: length of the message's format string as a 4-byte int
#Stage 2: the message's format string as a str
#Stage 3: the message itself as a tuple
#Assumes msg is a tuple of the form (x1,x2,...,xn) with any strings encoded as bytes and no "nested" tuples
#fmtstr is a str
#Condition data as such before calling the function

def send_msg(fmtstr,msg,port):
	try:
		#Stage 1: Send Length of message's format string
		fmtstrsize = len(fmtstr)
		stg1_msg = ustruct.pack('@i',fmtstrsize)
		port.write(stg1_msg)
		
		#Stage 2: Send The message's format string
		stg2_fmtstr = '@%is' % (fmtstrsize)
		stg2_msg = ustruct.pack(stg2_fmtstr,fmtstr.encode())
		port.write(stg2_msg)
		
		#Stage 3: Send The data
		stg3_msg = ustruct.pack(fmtstr,*msg)
		port.write(stg3_msg)
		return 1
	except:
		return -1
	
#Best way to read a line from the USB_VCP
def getln(port):
	while(1):
		if port.any():
			msg = port.readline()
			port.write(ustruct.pack('@i',1))
			break
	return msg #Returns raw bytes message
	
def recv_msg(port):

	stg1 = getln(port)
	fmtstr_size = ustruct.unpack('@3s',stg1)[0] # Receive stage 1- the size of the format string
	fmtstr_size = int(fmtstr_size.decode()) #Turns it back into an actual fucking number

	fmtstringception = '@%is' % fmtstr_size # The format string of the format string = fmtstringception
	#Receive stage 2 - the format string
	stg2 = getln(port)
	fmtstr = ustruct.unpack(fmtstringception,stg2)[0]
	fmtstr = fmtstr.decode()
	
	#Receive stage 3 - the Data
	stg3 = getln(port)
	data = ustruct.unpack(fmtstr,stg3)
			
	return data

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()
brd = pyb.USB_VCP()
brd.setinterrupt(-1)
led1 = pyb.LED(1)

#Listen for the command/trigger
while(brd.isconnected()):
	#Looks for initialization command
	cmd = recv_msg(brd)[0]
	if cmd.decode() == 'Nick Sucks':
		led1.on()

		
                                        
				
	
	

