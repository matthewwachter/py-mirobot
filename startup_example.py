from time import sleep

from mirobot import Mirobot



m = Mirobot(debug=True)
m.connect('com3')

sleep(3)

m.home_individual()

sleep(30)

m.disconnect()