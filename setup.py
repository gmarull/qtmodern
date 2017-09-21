#!/usr/bin/env python

import re
from setuptools import setup

_version = re.search(r'__version__\s+=\s+\'(.*)\'',
                     open('qtmodern/__init__.py').read()).group(1)

setup(name='qtmodern',
      version=_version,
      packages=['qtmodern'],
      description='Qt Widgets Modern User Interface',
      long_description=open('README.rst').read(),
      author='Gerard Marull-Paretas',
      author_email='gerardmarull@gmail.com',
      url='https://www.github.com/gmarull/qtmodern',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: User Interfaces'
      ],
      package_data={
          'qtmodern': ['resources/*']
      },
      install_requires=['qtpy>=1.3.1'])
