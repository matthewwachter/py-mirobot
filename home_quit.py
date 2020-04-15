from time import sleep
import sys
from .mirobot import Mirobot


def msg_cb(message):
    if not 'ok' in message.lower():
        print('>>'+message)
    #print('CB: ', message)

    #Interesting = False
    #if '<Idle,' in message:
        #Interesting = True
    #if Interesting:
        ##pass
        #print('CB: ', message)

def wait(msg):
    print(' waiting for ',msg,'... ', flush=True)
    x = input('continue...')
    #sleep(15)

m = Mirobot(debug=False)
portname = '/dev/ttyUSB0'
m.connect(portname)
#m.set_receive_callback(msg_cb)

delaytime = 1
i = 0
sleep(2)
m.home_simultaneous()

wait('homing  ... type <Enter><ctl>-C to completely exit.')

quit()
 
