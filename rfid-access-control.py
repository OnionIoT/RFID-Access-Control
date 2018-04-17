import sys, os, time
from OmegaExpansion import oledExp
from OmegaExpansion import relayExp
import subprocess
import json

#initializing the Relay and Oled Expansions, and block the lock if it's open
def initial_setup():
        status_oled = oledExp.driverInit()
        status_relay = relayExp.driverInit(7)	# 7 is the address of the Relay Expansion; 7 is when all relay switches are switched OFF
        check = relayExp.readChannel(7, 0)	# (7, 0) - again 7 is the address and 0 is the relay channel
        if check == 1:
                close_lock()
        with open('data.json') as json_file:	# Your UIDs could be different, make changes to the data.json file according to your settings
                data = json.load(json_file)
                return data['accepted']
        return None

#close the lock
def close_lock():
        relayExp.setChannel(7,0,0)		# Setting Relay with address 7, channel 0 and state is 0 (OFF)
        return
		
#open the lock
def open_lock():
        relayExp.setChannel(7,0,1)		# # Setting Relay with address 7, channel 0 and state is 1 (ON)
        return

#function to access the lock for 5 seconds, print the output on the OLED expansion and close the lock
def access_lock(uid):
        oledExp.write("Your UID is: " + uid)
        relayExp.setChannel(7,0,1)
        time.sleep(5)
        relayExp.setChannel(7,0,0)
        oledExp.clear()
        return

#constantly scan for the rfid tag presence
def __main__():
        # perform initial setup and read list of accepted tag uids from json file
        acceptedUids = initial_setup()
        if acceptedUids is None:
                print 'ERROR: could not read accepted UIDs from file'
                sys.exit(1)

        while 1:
				#assign a system call to a variable cmd and use it in uid subprocess
                cmd = "nfc-list | grep UID | sed -e 's/ //g' -e 's/^.*://'"
                uid = subprocess.check_output(cmd, shell=True).rstrip('\n')
                for acceptedUid in acceptedUids:
                        if(acceptedUid == uid):
                                access_lock(uid)
                                
if __name__ == '__main__':
    __main__()
