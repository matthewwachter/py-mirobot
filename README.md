# py-mirobot

#### Python version 3.7.6

License: MIT

[Matthew Wachter](https://www.matthewwachter.com)

[VT Pro Design](https://www.vtprodesign.com)

## Description

py-mirobot is a python module that can be used to control the [WLkata Mirobot](http://www.wlkata.com/site/index.html)

![Mirobot](/images/Mirobot_Solo_256.jpg)

This component uses the G code protocol to communicate with the Mirobot over a serial connection. The official **G code instruction set** and **driver download** can be found at the [WLkata Download Page](http://www.wlkata.com/site/downloads.html)

## Example Usage

```python
from time import sleep
from mirobot import Mirobot

# create an instance of the Mirobot Class
m = Mirobot(debug=True)
# connect to the com3 port
m.connect('com3')

# wait for the connection
sleep(3)

# start the homing routine
m.home_simultaneous()

# wait for 10 seconds
sleep(10)

# close the connection
m.disconnect()
```

## Communication Methods

- **send_msg(msg)** - Send a serial message.
	- **msg (str)** - The message to send.

- **is_connected()** - Return current connection state.

- **connect(portname, listen_callback=None)** - Open the serial connection.
	- **portname (str)** - The name of the com port to connect to (can be found in the Device Manager in windows)
	- **listen_callback (method)** - A callback method that takes a message arg (e.g. recieve_msg(message)).

- **set_receive_callback(receive_callback)** - Set or change the callback method for received messages.
	- **receive_callback (method)** - A callback method that takes a message arg (e.g. recieve_msg(message)).

- **disconnect()** - Close the serial connection.

## Command Methods

- **home_individual()** - Perform the homing routine on all axes one at a time.

- **home_simultaneous()** - Perform the homing routine on all axes at the same time.

- **set_hard_limit(state)** - Set the hard limit state (True by default). Careful with this one!
	- **state (bool)** - The state to be set.

- **set_soft_limit(state)** - Set the soft limit state (True by default). Careful with this one!
	- **state (bool)** - The state to be set.

- **unlock_shaft()** - Unlock the shaft enabling movement.

- **go_to_zero()** - Send each axis to its 0 position.

- **go_to_axis(a1, a2, a3, a4, a5, a6, speed)** - Send each axis to a specific position.
	- **a1 (float)** - Angle of axis 1.
	- **a2 (float)** - Angle of axis 2.
	- **a3 (float)** - Angle of axis 3.
	- **a4 (float)** - Angle of axis 4.
	- **a5 (float)** - Angle of axis 5.
	- **a6 (float)** - Angle of axis 6.
	- **speed (int)** - The velocity of the move.

- **increment_axis(a1, a2, a3, a4, a5, a6, speed)** - Increment each axis a specific amount.
	- **a1 (float)** - Angle increment of axis 1.
	- **a2 (float)** - Angle increment of axis 2.
	- **a3 (float)** - Angle increment of axis 3.
	- **a4 (float)** - Angle increment of axis 4.
	- **a5 (float)** - Angle increment of axis 5.
	- **a6 (float)** - Angle increment of axis 6.
	- **speed (int)** - The velocity of the move.

- **go_to_cartesian_ptp(x, y, z, a, b, c, speed)** - Point to point move to a Cartesian position.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **go_to_cartesian_lin(x, y, z, a, b, c, speed)** - Linear move to a Cartesian position.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **increment_cartesian_ptp(x, y, z, a, b, c, speed)** - Point to point increment in Cartesian space.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **increment_cartesian_lin(x, y, z, a, b, c, speed)** - Linear increment in Cartesian space.
	- **x (float)** - TX position.
	- **y (float)** - TY position.
	- **z (float)** - TZ position.
	- **a (float)** - RX position.
	- **b (float)** - RY position.
	- **c (float)** - RZ position.
	- **speed (int)** - The velocity of the move.

- **set_air_pump(pwm)** - Set the pwm of the pneumatic air pump.
	- **pwm** - The pulse width modulation frequency of the pneumatic air pump.

- **set_gripper(pwm)** - Set the pwm of the gripper.
	- **pwm** - The pulse width modulation frequency of the gripper.

# ```linuxdev``` branch

### Note: This branch (```linuxdev```) is designed to be used as a python module so it can be called from a higher level folder/directory.   If you want to do this you have to change the name of the project folder as follows:
```
> mv  py-mirobot pymirobot
```
because python importing cannot handle ```-``` in module names.
	
## Controller Class
A controller instance implements a blocking move call such that it does not return to your code until the move is completed. This
eliminates the need for hand tuning **sleep()** statements in your code between moves.  The robot does not react well to a series
of overlapping move commands. 



The class also implements a **pose()** object which is a convenient way to store a pose.  

- **MRController(m, replacecallback) **
    - **m (Mirobot)** your Mirobot instance
    - **replacecallback (boolean)**  if ```True``` save and restore an existing Mirobot callback before/after the move. 
    
    - **move(command, pose)**
        - **command (str)** - either 'ptp' or 'lin' selects the move type
        - **pose (pose)**  - cartesian move end point and orientation 

    - **gr_close()**   Close the gripper
    - ** gr_open()**  Open the gripper
    - **set_speed(speed_value) (int)** Set the speed (within 0-2500)

A useful function is

### ** wait(str) **  - Print ```"waiting for <str>"``` and wait for the user to press ```[ENTER]```

## Utilities

- **home_quit.py**   Does those things (but because of the threading a ```<ctl>-C``` is still required from the user).

- **gripper_test.py** Does some tests to verify gripper function. 


