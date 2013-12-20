#!/usr/bin/env python

from setuptools import setup, find_packages

import spacemouse


setup(
    name='spacemouse',
    version=spacemouse.__version__,
    author="Rolf Morel",
    author_email="rolfmorel@gmail.com",
    packages=find_packages(exclude="examples"),
    license='LGPLv3',
    install_requires=['evdev', 'pyudev'],
    platforms=['Linux'],
    entry_points={'console_scripts':
                  ('spacemouse = spacemouse.cli.main:main')
                  },
    description=("A free software driver for 3D/6DoF input devices")
)
