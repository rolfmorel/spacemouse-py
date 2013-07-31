import operator

from . import MIN_DEVIATION
from .wrapper import SpaceMouseEventMotion, SpaceMouseEventButton

__all__ = ('any_motion', 'no_motion', 'motion_right', 'motion_left',
           'motion_up', 'motion_down', 'motion_forward', 'motion_back',
           'motion_pitch_back', 'motion_pitch_forward', 'motion_yaw_left',
           'motion_yaw_right', 'motion_roll_right', 'motion_roll_left',
           'any_button', 'any_button_press', 'button0', 'button1',
           'not_button0_or_1')


def arg_between(val, low, high):
    return low <= val <= high

any_motion = \
    {SpaceMouseEventMotion: None}

no_motion = \
    {SpaceMouseEventMotion:
        {'x':
            {'function': arg_between,
             'arguments': (-MIN_DEVIATION, MIN_DEVIATION)
             },
         'y':
            {'function': arg_between,
             'arguments': (-MIN_DEVIATION, MIN_DEVIATION)
             },
         'z':
            {'function': arg_between,
             'arguments': (-MIN_DEVIATION, MIN_DEVIATION)
             },
         'rx':
            {'function': arg_between,
             'arguments': (-MIN_DEVIATION, MIN_DEVIATION)
             },
         'ry':
            {'function': arg_between,
             'arguments': (-MIN_DEVIATION, MIN_DEVIATION)
             },
         'rz':
            {'function': arg_between,
             'arguments': (-MIN_DEVIATION, MIN_DEVIATION)
             }
         }
     }

motion_right = \
    {SpaceMouseEventMotion:
        {'x':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

motion_left = \
    {SpaceMouseEventMotion:
        {'x':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

motion_up = \
    {SpaceMouseEventMotion:
        {'y':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

motion_down = \
    {SpaceMouseEventMotion:
        {'y':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

motion_forward = \
    {SpaceMouseEventMotion:
        {'z':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

motion_back = \
    {SpaceMouseEventMotion:
        {'z':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

motion_pitch_back = \
    {SpaceMouseEventMotion:
        {'rx':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

motion_pitch_forward = \
    {SpaceMouseEventMotion:
        {'rx':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

motion_yaw_left = \
    {SpaceMouseEventMotion:
        {'ry':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

motion_yaw_right = \
    {SpaceMouseEventMotion:
        {'ry':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }


motion_roll_right = \
    {SpaceMouseEventMotion:
        {'rz':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

motion_roll_left = \
    {SpaceMouseEventMotion:
        {'rz':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

any_button = \
    {SpaceMouseEventButton: None}

any_button_press = \
    {SpaceMouseEventButton:
        {'press':
            {'function': operator.eq,
             'arguments': (1,)
             }
         }
     }

button0 = \
    {SpaceMouseEventButton:
        {'bnum':
            {'function': operator.eq,
             'arguments': (0,)
             }
         }
     }

button1 = \
    {SpaceMouseEventButton:
        {'bnum':
            {'function': operator.eq,
             'arguments': (1,)
             }
         }
     }

not_button0_or_1 = \
    {SpaceMouseEventButton:
        {'bnum':
            {'function': operator.gt,
             'arguments': (1,)
             }
         }
     }
