# py-mirobot

#### Python version 3.7.6

License: MIT

[Matthew Wachter](https://www.matthewwachter.com)

[VT Pro Design](https://www.vtprodesign.com)

## Description

py-mirobot is a python module that can be used to control the [WLkata Mirobot](http://www.wlkata.com/site/index.html)

This component uses the G code protocol to communicate with the Mirobot over a serial connection. The official **G code instruction set** and **driver download** can be found at the [WLkata Download Page](http://www.wlkata.com/site/downloads.html)

## Example Usage

```python
from time import sleep
from mirobot import Mirobot


m = Mirobot(debug=True)
m.connect('com3')

sleep(3)

m.home_simultaneous()

sleep(10)

m.disconnect()
```