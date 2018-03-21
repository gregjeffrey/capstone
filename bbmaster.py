import struct,time
from serial import Serial


def send_msg(fmtstr,msg,port):
	try:
		#Stage 1: Send Length of message's format string
		#But it has to send it as an ascii string (and not an int) because fuck you
		fmtstrsize = len(fmtstr)
		numstr = '%03d' % fmtstrsize
		stg1_msg = struct.pack('@3s',numstr)
		port.write(stg1_msg)
		
		#Stage 2: Send The message's format string
		stg2_fmtstr = '@%is' % (fmtstrsize)
		stg2_msg = struct.pack(stg2_fmtstr,fmtstr.encode())
		port.write(stg2_msg)
		
		#Stage 3: Send The data
		stg3_msg = struct.pack(fmtstr,*msg)
		port.write(stg3_msg)
		return 1
	except:
		return -1

	

	
## Note: On the Beaglebone (in pyserial), the read() function is blocking
## I.E. It will read until the serial port's timeout is reached, OR
## until the given number of bytes have been read.
def recv_msg(port):
	try:
		#Receive stage 1: Size of the message's format string
		fmtstr_size = struct.unpack('@i',port.read(4))[0]

		#Receive stage 2: The message's format string
		fmtstr = struct.unpack('@s',port.read(fmtstr_size))[0]

		#Receive stage 3: The data/message
		datasize = struct.calcsize(fmtstr)
		data = struct.unpack(fmtstr,port.read(datasize))

		#Send receipt confirmation
		port.write(struct.pack('@i',1))
		return data
	except:
		port.write(struct.pack('@i',0))
		return -1


def send_trigger(prt):
	trigger = (b'Nick Sucks',)
	success = send_msg('@10s',trigger,prt) #Sends initialization trigger to the camera		
	return success

try:
	prt = Serial(port='/dev/ttyACM0',baudrate=9600,timeout=5)
	#prt = Serial(port='COM7',baudrate=9600,timeout=5)
except:
	prt = Serial(port='/dev/ttyACM1',baudrate=9600,timeout=5)
	pass

#send_trigger(prt)


##	if success:
##		#Sends moving averages of data to the camera
##		fmtstr = "@3i50p" #six integers and one 'Pascal' string of a fixed length (50 bytes)
##		data_tup = (1,2,3,b'Nick Sucks')
##		success = send_msg(fmtstr,data_tup,prt)
##		
##		#Waits for calculated data to be returned
##		#Uses same format string as the sent moving averages
##		data = recv_msg(prt)
##		
##		#Waits for image size to be returned
##		fmtstr = "@i"
##		msg = prt.read(struct.calcsize(fmtstr))
##		imgsize = struct.unpack(fmtstr,msg)[0]
##
##		#Waits for image to be sent back,based on calculated image size
##		img = prt.read(imgsize)
##
##		#Saves image to file
##		#filename = 'testimg.jpg'
##		#imgfile = open(filename,'w')
##		#imgfile.write(img)
##		#imgfile.close()
##
##		return img
                



	
		
		
		
