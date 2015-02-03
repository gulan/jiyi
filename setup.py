#!/usr/bin/env python

from distutils.core import setup

setup(name='jiyi',
      version='0.0.0',
      description='Flash Card Game',
      author='gulan',
      author_email='glen.wilder@gmail.com',
      py_modules = ['deck','machine'],
      scripts=['jiyi_web.py']
     )
