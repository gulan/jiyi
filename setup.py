#!/usr/bin/env python

from distutils.core import setup

# Manually: sqlite3 hsk1.db <jiyi/chinese_sql/hsk1.sql  

setup(name='jiyi',
      version='0.5.0',
      description='Flash Card Game',
      author='gulan',
      author_email='glen.wilder@gmail.com',
      packages = ['jiyi','jiyi.chinese_sql'],
      package_data = {'jiyi.chinese_sql' : ['hsk1.sql']},
      scripts=['jiyi_web.py'])
