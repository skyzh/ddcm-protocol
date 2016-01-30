#!/usr/bin/env python3

from distutils.core import setup

setup(
      name='DDCM',
      version='1.0',
      description='Dawn Distributed Computing Model',
      author='SkyZH',
      author_email='iSkyZH@gmail.com',
      url='https://github.com/SkyZH/ddcm-protocol',
      packages=[
            "ddcm",
            "ddcm.const.kad",
            "ddcm.TCPService"
      ],
      package_dir={'ddcm': 'ddcm'}
)
