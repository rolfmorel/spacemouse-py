
MIN_DEVIATION = 200

AXIS_MAP_SPACENAVD = False

# DRY, use __all__ definition
from .wrapper import *
from .event import EVENTS
# import here for normal import behaviour for library users, because of
# replacing the object in sys.modules
from . import register, monitor
