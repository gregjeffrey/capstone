import struct,time,dbConnect
from serial import Serial


def send_msg(fmtstr,msg,port):
	#Stage 1: Send Length of message's format string
	#But it has to send it as an ascii string (and not an int) because fuck you
	fmtstrsize = len(fmtstr)
	numstr = '%03d' % fmtstrsize
	stg1_msg = struct.pack('@3s',numstr)
	port.write(stg1_msg)
	
	#Stage 2: Send The message's format string
	stg2_fmtstr = '@%is' % (fmtstrsize)
	stg2_msg = struct.pack(stg2_fmtstr,fmtstr)
	port.write(stg2_msg)
	
	#Stage 3: Send The data
	stg3_msg = struct.pack(fmtstr,*msg)
	port.write(stg3_msg)
	
	return 1

## Note: On the Beaglebone (in pyserial), the read() function is blocking
## I.E. It will read until the serial port's timeout is reached, OR
## until the given number of bytes have been read.
def recv_msg(port):
	#Receive stage 1: Size of the message's format string
	fmtstr_size = struct.unpack('@i',port.read(4))[0]
	
	#Receive stage 2: The message's format string
	numstr = '@%is' % fmtstr_size
	fmtstr = struct.unpack(numstr,port.read(fmtstr_size))[0]

	#Receive stage 3: The data/message
	datasize = struct.calcsize(fmtstr)
	data = struct.unpack(fmtstr,port.read(datasize))

	if data:
		return data
	else:
		return -1

		
def recv_img(port,img_no):

	sz = struct.unpack('@i',port.read(4))[0]
	print 'Reading %i bytes: ' % sz
	img = port.read(sz)
	
	#Write the image to a file
	filename = 'testimg%i.jpg' % img_no
	imgfile = open(filename,'w')
	imgfile.write(img)
	imgfile.close()
	return filename

			
def send_trigger(port):
	trigger = (b'Go',)
	success = send_msg('@2s',trigger,port) #Sends initialization trigger to the camera		
	return success
	
def send_averages(port):
	fakedata = (1,2,3,4,5,6,b'Test String')
	success = send_msg('@6i11s',fakedata,port)
	return success


#Set up PySerial connection	
try:
	port = Serial(port='/dev/ttyACM0',baudrate=115200,timeout=5)
	port.inWaiting()
except:
	port = Serial(port='/dev/ttyACM1',baudrate=115200,timeout=5)	


(cnx,cur,ftp) = dbConnect.est_connections()

	
def mainloop(num):
	port.flushInput()
	send_trigger(port)
	send_averages(port)
	data = recv_msg(port)
	print data
	imgfile = recv_img(port,num)
	print 'Image saved at %s' % imgfile
	
	dbConnect.add_vals(cnx,cur)
	dbConnect.add_img(imgfile,ftp)
	
	print('Image uploaded!')
	
	return imgfile


	

                



	
		
		
		
