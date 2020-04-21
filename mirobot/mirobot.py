from pprint import pprint
import re
import sys

from .serial_device import SerialDevice
from .mirobot_status import MirobotStatus
from .exceptions import MirobotError, MirobotAlarm, MirobotReset, MirobotAmbiguousPort, MirobotStatusError, MirobotResetFileError, MirobotVariableCommandError


class Mirobot:
    def __init__(self, receive_callback=None, debug=False):
        self.debug = debug

        self.serial_device = SerialDevice()
        self.receive_callback = receive_callback

        self.get_status_callback = None

        # status

        self.status = MirobotStatus()

    # COMMUNICATION #

    # send a message
    def send_msg(self, msg, get_status=True):
        if self.is_connected():
            self.serial_device.send(msg,  terminator='\r\n')
        if self.debug:
            print('Message sent: ', msg)

        if get_status:
            self.get_status()

    # message receive handler
    def _receive_msg(self, msg):
        msg = msg.decode('utf-8')
        if self.debug:
            print('Message received:', msg)
        if self.receive_callback is not None:
            try:
                self.receive_callback(msg)
            except Exception as e:
                print(e)
                print('Receive callback error: ', sys.exc_info()[0])

        if msg.startswith('<'):
            self.update_status(msg)

    def update_status(self, msg):
        """ Update the status of the Mirobot. """
        self.status = self._parse_status(msg)

    def _parse_status(self, msg):
        """
        Parse the status strin
        g of the Mirobot and store the various values as class variables.

        Parameters
        ----------
        msg : str
            Status string that is obtained from a '?' instruction or `Mirobot.get_status` call.

        Returns
        -------
        return_status : MirobotStatus
            A new `mirobot.mirobot_status.MirobotStatus` object containing the new values obtained from `msg`.
        """

        return_status = MirobotStatus()

        state_regex = r'<([^,]*),Angle\(ABCDXYZ\):([-\.\d,]*),Cartesian coordinate\(XYZ RxRyRz\):([-.\d,]*),Pump PWM:(\d+),Valve PWM:(\d+),Motion_MODE:(\d)>'

        regex_match = re.fullmatch(state_regex, msg)

        if regex_match:
            try:
                state, angles, cartesians, pump_pwm, valve_pwm, motion_mode = regex_match.groups()
                self.status.state = state

                a, b, c, d, x, y, z = map(float, angles.split(','))

                return_status.angle.a = a
                return_status.angle.b = b
                return_status.angle.c = c
                return_status.angle.d = d
                return_status.angle.x = x
                return_status.angle.y = y
                return_status.angle.z = z

                x, y, z, a, b, c = map(float, cartesians.split(','))
                return_status.cartesian.x = x
                return_status.cartesian.y = y
                return_status.cartesian.z = z
                return_status.cartesian.a = a
                return_status.cartesian.b = b
                return_status.cartesian.c = c

                return_status.pump_pwm = int(pump_pwm)

                return_status.valve_pwm = int(valve_pwm)

                return_status.motion_mode = bool(motion_mode)

            except Exception as exception:
                raise Exception([MirobotStatusError(f'Could not parse status message "{msg}"'),
                                 exception])
            else:
                return return_status
        else:
            raise MirobotStatusError(f'Could not parse status message "{msg}"')

    # check if we are connected
    def is_connected(self):
        return self.serial_device.is_open

    # connect to the mirobot
    def connect(self, portname, receive_callback=None):
        self.serial_device.portname = portname
        self.serial_device.baudrate = 115200
        self.serial_device.stopbits = 1
        self.serial_device.listen_callback = self._receive_msg

        if receive_callback is not None:
            self.receive_callback = receive_callback

        self.serial_device.open()

    # set the receive callback
    def set_receive_callback(self, receive_callback):
        self.receive_callback = receive_callback

    # disconnect from the mirobot
    def disconnect(self):
        self.serial_device.close()

    # COMMANDS #

    # get the current status
    def get_status(self, callback=None):
        msg = '?'
        self.get_status_callback = callback
        self._send_msg(msg, get_status=False)

    # home each axis individually
    def home_individual(self):
        msg = '$HH'
        self.send_msg(msg, get_status=False)

    # home all axes simultaneously
    def home_simultaneous(self):
        msg = '$H'
        self.send_msg(msg, get_status=False)

    # set the hard limit state
    def set_hard_limit(self, state):
        msg = '$21=' + str(int(state))
        self.send_msg(msg, get_status=False)

    # set the soft limit state
    def set_soft_limit(self, state):
        msg = '$21=' + str(int(state))
        self.send_msg(msg, get_status=False)

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
