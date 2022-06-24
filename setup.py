#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup for `fed3`.

@author: Tom Earnest
"""

from setuptools import find_packages, setup

requirements = [
    'numpy>=1.2'
    'matplotlib>=3.4',
    'pandas>=1.3',
    'seaborn>=0.11'
    ]

setup(name='fed3',
      version='0.0.0',
      description='A Python package for analyzing FED3 data.',
      url='https://github.com/earnestt1234/fed3',
      author='Tom Earnest',
      author_email='earnestt1234@gmail.com',
      license='CC',
      packages=find_packages(),
      install_requires=requirements,
      include_package_data=True
	 )
