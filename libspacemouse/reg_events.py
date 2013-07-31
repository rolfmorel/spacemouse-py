import operator

from . import MIN_DEVIATION, AXIS_MAP_SPACENAVD
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

axis_x_pos = \
    {SpaceMouseEventMotion:
        {'x':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

axis_x_neg = \
    {SpaceMouseEventMotion:
        {'x':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

axis_y_pos = \
    {SpaceMouseEventMotion:
        {'y':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

axis_y_neg = \
    {SpaceMouseEventMotion:
        {'y':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

axis_z_pos = \
    {SpaceMouseEventMotion:
        {'z':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

axis_z_neg = \
    {SpaceMouseEventMotion:
        {'z':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

axis_rx_pos = \
    {SpaceMouseEventMotion:
        {'rx':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

axis_rx_neg = \
    {SpaceMouseEventMotion:
        {'rx':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }

axis_ry_pos = \
    {SpaceMouseEventMotion:
        {'ry':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

axis_ry_neg = \
    {SpaceMouseEventMotion:
        {'ry':
            {'function': operator.lt,
             'arguments': (-MIN_DEVIATION,)
             }
         }
     }


axis_rz_pos = \
    {SpaceMouseEventMotion:
        {'rz':
            {'function': operator.gt,
             'arguments': (MIN_DEVIATION,)
             }
         }
     }

axis_rz_neg = \
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

motion_right = axis_x_pos
motion_left = axis_x_neg
motion_up = axis_y_pos if AXIS_MAP_SPACENAVD else axis_z_neg
motion_down = axis_y_neg if AXIS_MAP_SPACENAVD else axis_z_pos
motion_forward = axis_z_pos if AXIS_MAP_SPACENAVD else axis_y_neg
motion_back = axis_z_neg if AXIS_MAP_SPACENAVD else axis_y_pos
motion_pitch_forward = axis_rx_neg
motion_pitch_back = axis_rx_pos
motion_yaw_left = axis_ry_pos if AXIS_MAP_SPACENAVD else axis_rz_neg
motion_yaw_right = axis_ry_neg if AXIS_MAP_SPACENAVD else axis_rz_pos
motion_roll_right = axis_rz_pos if AXIS_MAP_SPACENAVD else axis_ry_neg
motion_roll_left = axis_rz_neg if AXIS_MAP_SPACENAVD else axis_ry_pos
