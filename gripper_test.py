from time import sleep
import sys
from pymirobot.mirobot import Mirobot
import pymirobot.controller as ctlr_class
 
VERBOSITY = False

def wait(msg):
    print(' waiting for '+msg,flush=True)
    x = input('<Enter>')
    return x

m = Mirobot(debug=VERBOSITY)
portname = '/dev/ttyUSB0'
m.connect(portname)

sleep(2)   # wait for coms to sync up 
print('Robot is online...')

argc = len(sys.argv)
if argc > 1:
    if sys.argv[1].lower() == 'h':
        print('Homing')
        m.home_simultaneous()
        wait('Homing to complete')
        m.unlock_shaft()
else:
    m.unlock_shaft()


wait('user to start controller')


ctl = ctlr_class.MR_Controller(m)

defspeed = 400
ctl.set_speed(defspeed) 


# Default pose:
atx = 202.0
aty = 0.0
atz = 181.0
ata = 0.0
atb = 0.0
atc = 0.0
atgr = -32.0


p1 = ctlr_class.pose()
p1.x = 182
p1.y = 0
p1.z = 221

gdel = 1.5
print(' PWM Ramp test: ')
#for j in range (0,100,10):
    #p = j
    #print ('pwm: {}'.format(p))
    #m.set_gripper(p)
    #sleep(gdel)
    
#wait('user to verify PWM Ramp Test')

print('\n\n Controller Class open/close test:')
ntest = 5
for i in range(ntest):
    print('test {}/{}'.format(i+1, ntest))
    ctl.gr_open()
    print('gripper open')
    sleep(gdel) 
    ctl.gr_close()
    print('gripper close')
    sleep(gdel)


quit()


