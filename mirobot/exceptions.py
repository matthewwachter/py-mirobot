class MirobotError(Exception):
    """ An inplace class for throwing Mirobot errors. """
    pass


class MirobotAlarm(Warning):
    """  An inplace class for throwing Mirobot alarms. """
    pass


class MirobotReset(Warning):
    """ An inplace class for when Mirobot resets. """
    pass


class MirobotAmbiguousPort(Exception):
    """ An inplace class for when the serial port is unconfigurable. """
    pass


class MirobotStatusError(Exception):
    """ An inplace class for when Mirobot's status message is unprocessable. """
    pass


class MirobotResetFileError(Exception):
    """ An inplace class for when Mirobot has problems using the given reset file. """
    pass


class MirobotVariableCommandError(Exception):
    """ An inplace class for when Mirobot finds a command that does not match variable setting-command syntax. """
    pass
