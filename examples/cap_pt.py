#
#   
#

from time import sleep
import sys
#from .mirobot import Mirobot
from .serial_device import SerialDevice


global activeFlg
activeFlg = 0
global logfile
global ptname
ptname = '*none*'

def msg_cb(message):
    message = message.decode('utf-8')
    global activeFlg
    global logfile
    global ptname
    if '<Idle' in message:
        print(ptname+': '+message, file=logfile)
        print( '----', file=logfile)
    activeFlg = 0

def wait(msg):
    print(' waiting for ',msg,'... ', flush=True)
    x = input('continue...')
    #sleep(15)

ptname = input('Enter a name for this point: ')


logfname = 'taughtpointlog.txt'
logfile = open(logfname, 'a')

activeFlg = 0

portname = '/dev/ttyUSB0'

ser = SerialDevice()

ser.portname = portname
ser.baudrate = 115200
ser.stopbits = 1
ser.listen_callback =  msg_cb
ser.open()


activeFlg = 1
while activeFlg:
    print('.',end='',flush=True)
    sleep(0.25)

logfile.close()

quit()
 
