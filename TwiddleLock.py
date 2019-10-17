from datetime import datetime, timedelta
import spidev
import time
import os
import sys
import threading
import RPi.GPIO as GPIO
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

minnuets=0
seconds=0
milliseconds=0
show=True
back=False
delay = 0.2
track=0
inside=""
listtrack=8
Password=["L6","R5","L5"]
valid=[6,5,5]
empty=[]
keys=[]
TimeUP=False
pot_level=0
pot_volts=0
status="Waiting for Password"
delta=""
mode="Secure"

GPIO.setmode(GPIO.BCM)

# sensor channels
pot=0



GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def callback1(channel):
	#os.system("clear")
	#global outputs
	#outputs.clear()
	mode="Secure"
	Thread1 = threading.Thread(target=Timer)
	Thread2 = threading.Thread(target=Left)
	Thread3 = threading.Thread(target=Track)
	Thread4 = threading.Thread(target=Display)
	Thread2.start()
	Thread1.start()
	Thread3.start()
	Thread4.start()
	
def callback2(channel):
	#os.system("clear")
	#global outputs
	#outputs.clear()
	global mode
	mode="Unsecure"
	Thread1 = threading.Thread(target=Timer)
	Thread2 = threading.Thread(target=Left)
	Thread3 = threading.Thread(target=Track)
	Thread4 = threading.Thread(target=Display)
	Thread2.start()
	Thread1.start()
	Thread3.start()
	Thread4.start()
	
	
	

def Timer():
	time.sleep(40)
	global TimeUP
	TimeUP=True
	print("Time Out")
	
def Track():
	n=0
	global TimeUP
	global keys
	global  Password
	global pot_volts
	global status
	global valid
	global	empty
	while True:
		ver= pot_volts
		time.sleep(1.5)
		jay=pot_volts
		status="Waiting for Password"
		if (ver==jay):
			n+=1
		else:
			n=0
		if(n==3):
			if (mode=="Secure"):
				if(keys==Password):
					status="Password Correct!!!"
					break
				else:
					status="Incorrect Password"
					keys.clear()
					n=0
			else:
				if (set(valid)==set(empty)):
					status="Password Correct!!!"
					break
				else:
					status="Incorrect Password"
					keys.clear()
					n=0
					

def Display():
	global delta 
	rem=timedelta(seconds=40)
	n=0.1
	while True:
		time.sleep(0.1)
		n+=0.1
		delta=str(rem-timedelta(seconds=n))[5:-4]
		if(TimeUP):
			break
		
	
GPIO.add_event_detect(21, GPIO.FALLING, callback=callback1,bouncetime=200)
GPIO.add_event_detect(20, GPIO.FALLING, callback=callback2,bouncetime=200)



#timer to stop the progamme after time passes 

 
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  adc_val = ((adc[1]&3) << 8) + adc[2]
  return adc_val
 

def ConvertVolts(adc_val):
  volts = (adc_val * 3.3) / float(1023)
  volts = round(volts,1)
  return volts
 
def Left():
	global valid
	global	empty
	global pot_level
	global pot_volts
	global TimeUP
	global Password
	global keys
	global status
	start= datetime.now();
	global delta
	while True:

	  
		if(TimeUP):
			
			break
		os.system("clear")
		pot_level =ReadChannel(pot)
		pot_volts=ConvertVolts(pot_level)
		keeper=str(datetime.now()-start)[:-4]
		print("{} {}\t{}\t{} Time Remaining:{}".format(status,str(datetime.now()-start)[:-4],pot_volts,keys,delta))
		if pot_volts==0:
			keys.append("L"+str(int(keeper[5:-3])))
			empty.append(int(keeper[5:-3]))
			Right()
		
		
	  
		time.sleep(delay)
		

def Right():
	global valid
	global	empty
	global pot_level
	global pot_volts
	global TimeUP
	global Password
	global keys
	global status
	start= datetime.now();
	global delta
	while True:

	  
		if(TimeUP):
			
			break
		os.system("clear")
		pot_level =ReadChannel(pot)
		pot_volts=ConvertVolts(pot_level)
		keeper=str(datetime.now()-start)[:-4]
		print("{} {}\t{}\t{} Time Remaining:{}".format(status,str(datetime.now()-start)[:-4],pot_volts,keys,delta))
		if pot_volts==3.3:
			keys.append("R"+str(int(keeper[5:-3])))
			empty.append(int(keeper[5:-3]))
			Left()
		
		
	  
		time.sleep(delay)

while True:
	time.sleep(0.1)
 



 


  

