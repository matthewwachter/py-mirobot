from threading import Thread

from serial_device import SerialDevice


class Mirobot:
    def __init__(self, receive_callback=None, debug=False):
        # The component to which this extension is attached
        self.serial_device = SerialDevice()
        self.receive_callback = receive_callback
        self.debug = debug

    ### COMMUNICATION ###

    # send a message
    def send_msg(self, msg):
        if self.is_connected():
            self.serial_device.send(msg,  terminator='\r\n')
        if self.debug:
            print('Message sent: ', msg)

    # message receive handler
    def _receive_msg(self, msg):
        msg = msg.decode('utf-8')
        if self.debug:
            print('Message received:', msg)
        if self.receive_callback is not None:
            try:
                self.receive_callback(msg)
            except:
                print('Receive callback error: ', sys.exc_info()[0])

    # check if we are connected
    def is_connected(self):
        return self.serial_device.is_open

    # connect to the mirobot
    def connect(self, portname, listen_callback=None):
        self.serial_device.portname = portname
        self.serial_device.baudrate = 115200
        self.serial_device.stopbits = 1
        self.serial_device.listen_callback = self._receive_msg
        self.serial_device.open()

    # set the receive callback
    def set_receive_callback(self, receive_callback):
        self.receive_callback = receive_callback

    # disconnect from the mirobot
    def disconnect(self):
        self.serial_device.close()


    ### COMMANDS ###

    # home each axis individually
    def home_individual(self):
        msg = '$HH'
        self.send_msg(msg)

    # home all axes simultaneously
    def home_simultaneous(self):
        msg = '$H'
        self.send_msg(msg)

    # set the hard limit state
    def set_hard_limit(self, state):
        msg = '$21=' + str(int(state))
        self.send_msg(msg)

    # set the soft limit state
    def set_soft_limit(self, state):
        msg = '$21=' + str(int(state))
        self.send_msg(msg)

    # unlock the shaft
    def unlock_shaft(self):
        msg = 'M50'
        self.send_msg(msg)

    # send all axes to their respective zero positions
    def go_to_zero(self):
        self.go_to_axis(0, 0, 0, 0, 0, 0, 2000)

    # send all axes to a specific position
    def go_to_axis(self, a1, a2, a3, a4, a5, a6, speed):
        msg = 'M21 G90'
        msg += ' X' + str(a1)
        msg += ' Y' + str(a2)
        msg += ' Z' + str(a3)
        msg += ' A' + str(a4)
        msg += ' B' + str(a5)
        msg += ' C' + str(a6)
        msg += ' F' + str(speed)
        self.send_msg(msg)
        return

    # increment all axes a specified amount
    def increment_axis(self, a1, a2, a3, a4, a5, a6, speed):
        msg = 'M21 G91'
        msg += ' X' + str(a1)
        msg += ' Y' + str(a2)
        msg += ' Z' + str(a3)
        msg += ' A' + str(a4)
        msg += ' B' + str(a5)
        msg += ' C' + str(a6)
        msg += ' F' + str(speed)
        self.send_msg(msg)
        return

    # point to point move to a cartesian position
    def go_to_cartesian_ptp(self, x, y, z, a, b, c, speed):
        msg = 'M20 G90 G0'
        msg += ' X' + str(x)
        msg += ' Y' + str(y)
        msg += ' Z' + str(z)
        msg += ' A' + str(a)
        msg += ' B' + str(b)
        msg += ' C' + str(c)
        msg += ' F' + str(speed)
        self.send_msg(msg)
        return

    # linear move to a cartesian position
    def go_to_cartesian_lin(self, x, y, z, a, b, c, speed):
        msg = 'M20 G90 G1'
        msg += ' X' + str(x)
        msg += ' Y' + str(y)
        msg += ' Z' + str(z)
        msg += ' A' + str(a)
        msg += ' B' + str(b)
        msg += ' C' + str(c)
        msg += ' F' + str(speed)
        self.send_msg(msg)
        return

    # point to point increment in cartesian space
    def increment_cartesian_ptp(self, x, y, z, a, b, c, speed):
        msg = 'M20 G91 G0'
        msg += ' X' + str(x)
        msg += ' Y' + str(y)
        msg += ' Z' + str(z)
        msg += ' A' + str(a)
        msg += ' B' + str(b)
        msg += ' C' + str(c)
        msg += ' F' + str(speed)
        self.send_msg(msg)
        return

    # linear increment in cartesian space
    def increment_cartesian_lin(self, x, y, z, a, b, c, speed):
        msg = 'M20 G91 G1'
        msg += ' X' + str(x)
        msg += ' Y' + str(y)
        msg += ' Z' + str(z)
        msg += ' A' + str(a)
        msg += ' B' + str(b)
        msg += ' C' + str(c)
        msg += ' F' + str(speed)
        self.send_msg(msg)
        return

    # set the pwm of the air pump
    def set_air_pump(self, pwm):
        msg = 'M3S' + str(pwm)
        self.send_msg(msg)

    # set the pwm of the gripper
    def set_gripper(self, pwm):
        msg = 'M4E' + str(pwm)
        self.send_msg(msg)
