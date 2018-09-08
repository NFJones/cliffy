#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages

requirements = []
with open('./requirements.txt', 'r') as infile:
    for line in infile:
        requirements.append(line.replace('\n', '').replace('\r', ''))

setup(name='cliffy',
      version='0.0.1',
      description='A convenient CLI wrapper for other command line programs.',
      author='Neil F Jones',
      author_email='neil.franklin.jones@gmail.com',
      url='https://github.com/NFJones/cliffy.git',
      packages=find_packages(),
      include_package_data=True,
      scripts=['cliffy/cliffy.py'],
      install_requires=requirements)
