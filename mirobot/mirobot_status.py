from dataclasses import dataclass

@dataclass
class MirobotAngleValues:
    """ A dataclass to hold Mirobot's angular values. """
    a: float = 0.0
    """ Angle of axis 1 """
    b: float = 0.0
    """ Angle of axis 2 """
    c: float = 0.0
    """ Angle of axis 3 """
    x: float = 0.0
    """ Angle of axis 4 """
    y: float = 0.0
    """ Angle of axis 5 """
    z: float = 0.0
    """ Angle of axis 6 """
    d: float = 0.0
    """ Location of rail or stepper module """

@dataclass
class MirobotCartesianValues:
    """ A dataclass to hold Mirobot's cartesian values and roll/pitch/yaw angles. """
    x: float = 0.0
    """ Position on X-axis """
    y: float = 0.0
    """ Position of Y-axis """
    z: float = 0.0
    """ Position of Z-axis """
    a: float = 0.0
    """ Position of Roll angle """
    b: float = 0.0
    """ Position of Pitch angle """
    c: float = 0.0
    """ Position of Yaw angle """

@dataclass
class MirobotStatus:
    """ A composite dataclass to hold all of Mirobot's trackable quantities. """
    state: str = ''
    """ The brief descriptor string for Mirobot's state. """
    angle: MirobotAngleValues = MirobotAngleValues()
    """ Dataclass that holds Mirobot's angular values including the rail position value. """
    cartesian: MirobotCartesianValues = MirobotCartesianValues()
    """ Dataclass that holds the cartesian values and roll/pitch/yaw angles. """
    pump_pwm: int = 0
    """ The current pwm of the pnuematic pump module. """
    valve_pwm: int = 0
    """ The current pwm of the value module. (eg. gripper) """
    motion_mode: bool = False
    """ Whether Mirobot is currently in coordinate mode or joint-motion mode """
