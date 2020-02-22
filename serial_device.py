import serial
import sys
from threading import Thread

class SerialDevice:
    def __init__(self, portname='', baudrate=0, stopbits=1, listen_callback=None):
        self.portname = portname
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.timeout = None
        self.listen_callback = None
        self.listen_thread = None
        self.serialport = serial.Serial()
        self._is_open = False

    # close the serial port when the class is deleted
    def __del__(self):
        try:
            if self._is_open:
                self.serialport.close()
        except:
            print("Destructor error closing COM port: ", sys.exc_info()[0] )

    # check if the serial port is open
    @property
    def is_open(self):
        self._is_open = self.serialport.is_open
        return self._is_open

    # sets the listen callback
    def set_listen_callback(self, listen_callback):
        if self.listen_thread is not None:
            self.listen_thread.stop()

        self.listen_callback = listen_callback

        if self._is_open:
            self.start_listen_thread()

    # starts the listen thread
    def start_listen_thread(self):
        if self.listen_callback is not None:
            self.listen_thread = Thread(target=self.listen_to_device, args=(self.listen_callback,)).start()


    # listen to the serial port and pass the message to the callback
    def listen_to_device(self, listen_callback):
        while self._is_open:
            try:
                msg = self.serialport.readline()
                if msg != "":
                    if listen_callback is not None:
                        listen_callback(msg)
            except:
                print("Error reading COM port: ", sys.exc_info()[0])

    # open the serial port
    def open(self):
        if not self._is_open:
            # serialport = 'portname', baudrate, bytesize = 8, parity = 'N', stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = self.portname
            self.serialport.baudrate = self.baudrate
            self.serialport.stopbits = self.stopbits
            try:
                self.serialport.open()
                self._is_open = True
                self.start_listen_thread()
            except:
                print("Error opening COM port: ", sys.exc_info()[0])

    # close the serial port
    def close(self):
        if self._is_open:
            try:
                self._is_open = False
                self.serialport.close()
            except:
                print("Close error closing COM port: ", sys.exc_info()[0])

    # send a message to the serial port
    def send(self, message, terminator='\r\n'):
        if self._is_open:
            try:
                message += terminator
                self.serialport.write(message.encode('utf-8'))
            except:
                print("Error sending message: ", sys.exc_info()[0] )
            else:
                return True
        else:
            return False