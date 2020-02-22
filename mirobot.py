from threading import Thread

from serial_device import SerialDevice

class Mirobot:
	"""
	Mirobot description
	"""
	def __init__(self, portname, receive_callback):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.serial_device = SerialDevice()

	### COMMUNICATION

	def is_connected(self):
		return self.serial_device.is_open()

	def open_connection(self, portname, listen_callback=None):
		self.serial_device.portname = portname
		self.serial_device.baudrate = 15200
		self.serial_device.stopbits = 1
		self.serial_device.listen_callback = listen_callback
		self.serial_device.open()

	def close_connection():
		self.serial_device.close()

	def _send_msg(self, msg):
		if self.is_connected():
			self.serial_device.send(msg,  terminator='\r\n')

	### COMMANDS

	def home_individual(self):
		msg = '$HH'
		self.send_msg(msg)

	def home_simultaneous(self):
		msg = '$H'
		self.send_msg(msg)

	def set_hard_limit(self, state):
		msg = '$21=' + str(int(state))
		self.send_msg(msg)

	def set_soft_limit(self, state):
		msg = '$21=' + str(int(state))
		self.send_msg(msg)

	def unlock_shaft(self):
		msg = 'M50'
		self.send_msg(msg)

	def go_to_zero(self):
		self.GoToAxis(0, 0, 0, 0, 0, 0, 2000)

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

	def set_air_pump(self, pwm):
		msg = 'M3S' + str(pwm)
		self.send_msg(msg)

	def set_gripper(self, pwm):
		msg = 'M4E' + str(pwm)
		self.send_msg(msg)