from time import sleep
import sys
from .mirobot import Mirobot

global ok_count
ok_count = 0
global runstate
runstate = 0
def msg_cb(message):
    global ok_count
    global runstate
    if 'ok' in message.lower():
        ##print('>>'+message )
        ##print('>> {} oks'.format(ok_count))
        runstate = 0
    if '<Run' in message:
        runstate = 1
    if 'Idle' in message:
        runstate = 0
     
        
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

m = Mirobot(debug=True)
portname = '/dev/ttyUSB0'
m.connect(portname)
m.set_receive_callback(msg_cb)

delaytime = 1
i = 0
sleep(1)

argc = len(sys.argv)
if argc > 1:
    if sys.argv[1].lower() == 'h':
        m.home_simultaneous()
        sleep(delaytime)
        wait('Homing')
else:
    m.unlock_shaft()
    
delta = 10
speed = 800
#m.increment_cartesian_lin(x, y, z, a, b, c, speed) - Linear increment in Cartesian space.

#print('Startup Example: going to zero')
#m.go_to_zero()
#wait('motion to zero')

attn_str = '<Idle,Angle(ABCDXYZ):-121.000,26.013,7.381,0.000,98.854,7.483,-32.000,Cartesian coordinate(XYZ RxRyRz):-8.317,178.506,279.800,-105.753,-28.260,68.962,Pump PWM:0,Valve PWM:0,Motion_MODE:0>'

atx = -8.3
aty = 178.5
atz = 279.8
ata = -105.75
atb = -28.3
atc = 69.0
atgr = -32.0

# if homing correctly goes to pose of Figure 1.1

atx = 202.0
aty = 0.0
atz = 181.0
ata = 0.0
atb = 0.0
atc = 0.0
atgr = -32.0

#print('Startup Example: Go to "attention"')
##m.go_to_cartesian_ptp(atx, aty, atz, ata, atb, atc,  speed) # - Linear absolute in Cartesian space.
#m.go_to_cartesian_lin(atx, aty, atz, ata, atb, atc,  speed) # - Linear absolute in Cartesian space.
#wait('Attention Pose')


#
#  Make a square with relative cartesian moves
#
x = input(' initiate the move sequences: ')


i += 1
print('Startup Example: move ',i,flush=True)

for j in range(4):
    runstate = 1
    m.increment_cartesian_lin(0,10,0,0,0,0, speed) # - Linear increment in Cartesian space.
    while(runstate==1):
        sleep(0.25)

    i += 1
    runstate = 1
    print('Startup Example: move ',i,flush=True)
    m.increment_cartesian_lin(10,0,0,0,0,0, speed) # - Linear increment in Cartesian space.
    while(runstate==1):
        sleep(0.25)


    i += 1
    runstate = 1
    print('Startup Example: move ',i,flush=True)
    m.increment_cartesian_lin(0,-10,0,0,0,0, speed) # - Linear increment in Cartesian space.
    while(runstate==1):
        sleep(0.25)


    i += 1
    runstate = 1
    print('Startup Example: move ',i,flush=True)
    m.increment_cartesian_lin(-10,0,0,0,0,0, speed) # - Linear increment in Cartesian space.
    while(runstate==1):
        sleep(0.25)


#m.disconnect()
print('All Done')
quit()

