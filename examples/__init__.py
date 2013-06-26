# try to import libspacemouse from system else setup path for import from
# parent directory
try:
    import libspacemouse
except ImportError:
    import sys
    import os
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not path in sys.path:
        sys.path.append(path)
