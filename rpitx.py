#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess
import time
import os
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
transmit = False
if GPIO.input(12) == False:
	transmit = True
if GPIO.input(27) == False:
	transmit = True
	txLed = 22
	txLedOn = False
 	txLedOff = True
else:
	txLed = 27
	txLedOn = True
 	txLedOff = False
	
GPIO.setup(txLed, GPIO.OUT)
	
print(transmit)

file = open("/home/pi/CubeSatSim/sim.cfg")
callsign = file.readline().split(" ")[0]
print(callsign)

GPIO.output(txLed, txLedOn);
os.system("echo 'de " + callsign + "' > id.txt && gen_packets -M 20 id.txt -o morse.wav -r 48000 > /dev/null 2>&1 && cat morse.wav | csdr convert_i16_f | csdr gain_ff 7000 | csdr convert_f_samplerf 20833 | sudo /home/pi/rpitx/rpitx -i- -m RF -f 434.9e3")
GPIO.output(txLed, txLedOff);

time.sleep(2)

if __name__ == "__main__":
	
  if (transmit):
	
    print 'Length: ', len(sys.argv)
    
    if (len(sys.argv)) > 1:
#        print("There are arguments!")
        if (('a' == sys.argv[1]) or ('afsk' in sys.argv[1])):
            print("AFSK") 
	    while True:
    		time.sleep(5)
        elif (('s' == sys.argv[1]) or ('sstv' in sys.argv[1])):
            print("SSTV")
	    GPIO.output(txLed, txLedOn);
	    os.system("(while true; do (sleep 5 && cat /home/pi/CubeSatSim/wav/sstv.wav); done) | csdr convert_i16_f | csdr gain_ff 7000 | csdr convert_f_samplerf 20833 | sudo rpitx -i- -m RF -f 434.9e3")
#	    while True:
#		GPIO.output(txLed, txLedOff);
#		print("Sleeping")
#		time.sleep(10)
#		print("Transmitting SSTV")
#		GPIO.output(txLed, txLedOn);
#		os.system("cat /home/pi/CubeSatSim/wav/sstv.wav | csdr convert_i16_f | csdr gain_ff 7000 | csdr convert_f_samplerf 20833 | sudo rpitx -i- -m RF -f 434.9e3")
	elif (('b' == sys.argv[1]) or ('bpsk' in sys.argv[1])):
            print("BPSK")
	    os.system("sudo nc -l 8080 | csdr convert_i16_f | csdr fir_interpolate_cc 2 | csdr dsb_fc | csdr bandpass_fir_fft_cc 0.002 0.06 0.01 | csdr fastagc_ff | sudo /home/pi/rpitx/sendiq -i /dev/stdin -s 96000 -f 434.9e6 -t float")
	else:
            print("FSK") 
	    os.system("sudo nc -l 8080 | csdr convert_i16_f | csdr gain_ff 7000 | csdr convert_f_samplerf 20833 | sudo /home/pi/rpitx/rpitx -i- -m RF -f 434.9e3")
    else:
        print("FSK") 
	os.system("sudo nc -l 8080 | csdr convert_i16_f | csdr gain_ff 7000 | csdr convert_f_samplerf 20833 | sudo /home/pi/rpitx/rpitx -i- -m RF -f 434.9e3")
  else:
    print("No Band Pass Filter so no telemetry transmit.  See http://cubesatsim.org/wiki for instructions on how to build the BPF.")
    while True:
      time.sleep(5)
