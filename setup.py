#!/usr/bin/env python

import qtmodern
from setuptools import setup

_version = qtmodern.__version__

setup(name='qtmodern',
      version=_version,
      packages=['qtmodern'],
      description='Qt Widgets Modern User Interface',
      long_description=open('README.rst').read(),
      author='Gerard Marull-Paretas',
      author_email='gerardmarull@gmail.com',
      url='https://www.github.com/gmarull/qtmodern',
      license='MIT',
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
