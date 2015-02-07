#!/usr/bin/env python

from distutils.core import setup

# manually: sqlite hsk1.db <hsk1.sql  

setup(name='jiyi',
      version='0.1.0',
      description='Flash Card Game',
      author='gulan',
      author_email='glen.wilder@gmail.com',
      py_modules = ['deck','machine'],
      scripts=['jiyi_web.py']
     )
