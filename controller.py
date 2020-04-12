#from threading import Thread 
from time import sleep
import sys
from .mirobot import Mirobot

# if homing correctly goes to pose of Figure 1.1

atx = 202.0
aty = 0.0
atz = 181.0
ata = 0.0
atb = 0.0
atc = 0.0
atgr = -32.0

global ok_count
ok_count = 0
global runstate
runstate = 0
        

class pose():
    def __init__(self):
        self.x = atx
        self.y = aty
        self.z = atz
        self.a = ata
        self.b = atb
        self.c = atc
    def set_position(X):
        self.x = X[0]
        self.y = X[1]
        self.z = X[2]
    def set_rotation_XYZ(R):
        self.a = R[0]
        self.b = R[1]
        self.c = R[2]
        
class MR_Controller(): 
    '''
    allow motion commands which BLOCK until completion (no sleeps!)

    '''

    def __init__(self,m,replacecallback=False):
        self.repCB = replacecallback
        self.m = m
        self.Running = False
        self.old_callback = None
        # Attach Controller callback 
        m.set_receive_callback(self.ctl_cb2)

        self.speed = 500
        
    def move(self,command, pose):
        global runstate
        if command not in ['ptp', 'lin']:
            self.error('unknown command: '+command)
        self.Running = True
        runstate = 1
        target_args = '{:6.2f}, {:6.2f}, {:6.2f}, {:6.2f}, {:6.2f}, {:6.2f}, {:6.2f}'.format(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c, self.speed)
        #go_to_cartesian_ptp(x, y, z, a, b, c, speed) - Point to point move to a Cartesian position
        # start robot motion
        # stash the current coms callback
        if self.repCB:
            self.old_callback = self.m.get_receive_callback()
            # insert the controller cb
            self.m.set_receive_callback(self.ctl_cb2)
        if command == 'ptp':
            print('ctl.move: self.m.go_to_cartesian_ptp('+target_args+')')
            self.m.go_to_cartesian_ptp(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c, self.speed)
        elif command == 'lin':
            print('ctl.move: self.m.go_to_cartesian_lin('+target_args+')')
            self.m.go_to_cartesian_lin(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c, self.speed)
    
        sleep(0.25) # allow mvt to start
        while runstate == 1:
            print('m',end='',flush=True)
            sleep(0.25)
            self.m.get_status() # cause robot to report status
            
        if self.repCB:
            # restore the stashed cb
            self.m.set_receive_callback(self.old_callback)
        
    def ctl_cb2(self,message):
        global ok_count
        global runstate 
        symbol = '.'+str(runstate)+' '
        #if 'ok' in message.lower():
            ##print('>>'+message )
            ##print('>> {} oks'.format(ok_count))
            #runstate = 0 
        if '<Run' in message:
            #runstate = 1
            symbol = '/'+str(runstate)+' '
            pass
        if 'Idle' in message:
            symbol = '+'+str(runstate)+' '
            runstate = 0 
        if 'Soft limit' in message:
            self.error(message)
            
        print(symbol,end='',flush=True)   
            
    def gr_open(self):
        self.m.set_gripper(65)
        
    def gr_close(self):
        self.m.set_gripper(-32)
        
    def set_speed(self,sp): 
        if sp < 0 or sp > 2500:
            self.error('illegal speed')
        else:
            self.speed = float(sp)
            
    def error(self, msg):
        print('\n\n')
        print('Mirobot controller ERROR: ', msg)
        print('ctl-C to exit')
        quit()
        


########################3

def msg_cb(message):
    pass
    #print('CB: ', message)

    #Interesting = False
    #if '<Idle,' in message:
        #Interesting = True
    #if Interesting:
        ##pass
        #print('CB: ', message)

def wait(msg):
    print(' waiting for ',msg,'... ', flush=True)
    x = input('<Enter> to continue...')
    #sleep(15)
    
##############################################################################    Test
if __name__=='__main__':
    print('Test the blocking controller')
    
    m = Mirobot(debug=False)
    portname = '/dev/ttyUSB0'
    m.connect(portname)

    sleep(3)   # wait for coms to sync up 
    print('Robot is online...')
    
    argc = len(sys.argv)
    if argc > 1:
        if sys.argv[1].lower() == 'h':
            m.home_simultaneous()
            wait('Homing')
            m.unlock_shaft()
    else:
        m.unlock_shaft()


    wait('about to start controller')


    ctl = MR_Controller()
    m.set_receive_callback(ctl.ctl_cb2)

    g0 = pose()
    
    g1 = pose()  # "attention" by default
    g1.x -= 50.0
    g1.y -= 50.0
    g1.z += 50
    
    g2 = pose()
    g2.x += 20.0   # g2 is a different point
    
    
    g3 = pose()
    g3.y += 25.0
    g3.z += -10.0   # a third pose

        
    delta = 10
    defspeed = 400
    ctl.set_speed(defspeed) 
    d = 4
    
    wait('starting to move')
    
    for i in range(4):        
        ctl.move(m,'ptp',g0)
        print('completed g0 move')
        ctl.move(m, 'ptp',g1)
        print('completed g1 move')
        ctl.move(m, 'ptp',g2)
        print('completed g2 move')
        ctl.move(m, 'ptp',g3)
        print('completed g3 move')
        print('\nCompleted sequence '+str(i)+'\n')

        
    
