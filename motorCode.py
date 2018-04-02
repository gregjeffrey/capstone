import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time

#*****************************************************
pwmChannel1 = "P9_14" # Clockwise
pwmChannel2 = "P8_13" # Counterclockwise
optoChannel = "P9_15"

revsPerPlant = 4
totalPlants = 4
#*****************************************************

currentRevs = 0
currentPlant = 0

GPIO.setup(optoChannel, GPIO.IN)

PWM.start(pwmChannel1, 0, 10000)
print ("here")
while currentPlant < totalPlants:
    print ("plant: " + str(currentPlant))
    PWM.set_duty_cycle(pwmChannel1, 10)
    while currentRevs < revsPerPlant:
        print (currentRevs)
        GPIO.wait_for_edge(optoChannel, GPIO.FALLING)
        currentRevs += 1
    PWM.set_duty_cycle(pwmChannel1, 0)
    currentPlant += 1
    currentRevs = 0
    time.sleep(5)
    #*****************************************************
    # send trigger to start taking pics
    # some sort of trigger to move on - this trigger needs to come from knowing we are done with pics
    #*****************************************************
PWM.stop(pwmChannel1)
PWM.cleanup()
time.sleep(10)
currentRevs = 0
PWM.start(pwmChannel2, 0, 10000)
PWM.set_duty_cycle(pwmChannel2, 10)
print ("going back")
while currentRevs < (totalPlants * revsPerPlant):
    print (currentRevs)
    GPIO.wait_for_edge(optoChannel, GPIO.FALLING)
    currentRevs += 1
PWM.stop(pwmChannel2)
PWM.cleanup()