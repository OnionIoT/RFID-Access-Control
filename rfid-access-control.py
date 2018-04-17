import sys, os, time
from OmegaExpansion import oledExp
from OmegaExpansion import relayExp
import subprocess
import json

#initializing the Relay and Oled Expansions, and block the lock if it's open
def initial_setup():
        status_oled = oledExp.driverInit()
        status_relay = relayExp.driverInit(7)
        check = relayExp.readChannel(7, 0)
        if check == 1:
                close_lock()
        with open('data.json') as json_file:
                data = json.load(json_file)
                return data['accepted']
        return None

#close the lock
def close_lock():
        relayExp.setChannel(7,0,0)
        return
		
#open the lock
def open_lock():
        relayExp.setChannel(7,0,1)
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