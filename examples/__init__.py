# if a script is called using python module call (python -m examples.simple)
# add parent path to module path lookup

import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.append(path)
