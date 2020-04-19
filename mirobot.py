from pprint import pprint
import re
import sys

from serial_device import SerialDevice


class Mirobot:
    def __init__(self, receive_callback=None, debug=False):
        self.debug = debug

        self.serial_device = SerialDevice()
        self.receive_callback = receive_callback

        self.get_status_callback = None

        # status

        self.status = {
            'state': None,
            'angle': {
                'a1': 0.0,
                'a2': 0.0,
                'a3': 0.0,
                'a4': 0.0,
                'a5': 0.0,
                'a6': 0.0,
                'rail': 0.0,
            },
            'cartesian': {
                'tx': 0.0,
                'ty': 0.0,
                'tz': 0.0,
                'rx': 0.0,
                'ry': 0.0,
                'rz': 0.0,
            },
            'pump_pwm': 0,
            'valve_pwm': 0,
            'motion_mode': 0,
        }

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
            self._recv_status(msg)

    def _recv_status(self, msg):
        pars = self.ownerComp.par

        msg = msg.strip('<').strip('>')

        state = msg.split(',')[0]
        if state is not None:
            pars.Status = state

        msg = ','.join(msg.split(',')[1:])

        angle = re.match(r'Angle\(ABCDXYZ\):(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),', msg)

        if angle is not None:
            a4, a5, a6, rail, a1, a2, a3 = angle.groups()

            self.status['angle']['a1'] = float(a1)
            self.status['angle']['a2'] = float(a2)
            self.status['angle']['a3'] = float(a3)
            self.status['angle']['a4'] = float(a4)
            self.status['angle']['a5'] = float(a5)
            self.status['angle']['a6'] = float(a6)

        cart = re.match(r'.*Cartesian\scoordinate\(XYZ\sRxRyRz\):(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),', msg)
        if cart is not None:
            tx, ty, tz, rx, ry, rz = cart.groups()
            self.status['cartesian']['tx'] = float(tx)
            self.status['cartesian']['ty'] = float(ty)
            self.status['cartesian']['tz'] = float(tz)
            self.status['cartesian']['rx'] = float(rx)
            self.status['cartesian']['ry'] = float(ry)
            self.status['cartesian']['rz'] = float(rz)

        pump_pwm = re.match(r'.*Pump\sPWM:(\d+)', msg)
        if pump_pwm is not None:
            self.status['pump_pwm'] = int(pump_pwm.groups(0)[0])

        valve_pwm = re.match(r'.*Valve\sPWM:(\d+)', msg)
        if valve_pwm is not None:
            self.status['valve_pwm'] = int(valve_pwm.groups(0)[0])

        motion_mode = re.match(r'.*Motion_MODE:(\d+)', msg)
        if motion_mode is not None:
            self.status['motion_mode'] = int(motion_mode.groups(0)[0])

        if self.get_status_callback is not None:
            self.get_status_callback(self.status)

        if self.debug:
            pprint(self.status)

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
