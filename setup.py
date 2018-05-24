#!/usr/bin/env python3

import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
  long_description = f.read()

setuptools.setup(
  name='everything-efu-gen',
  version='0.0.2',

  description='Generator of Everything File List (EFU) files',
  long_description=long_description,

  url='https://github.com/tobbez/everything-efu-gen',

  author='tobbez',
  author_email='tobbez@ryara.net',

  license='ISC',

  py_modules=['everything_efu_gen'],

  entry_points={
    'console_scripts': [
      'everything-efu-gen=everything_efu_gen:main',
    ],
  },

  install_requires=['ruamel.yaml'],

  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: ISC License (ISCL)',

    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],

  keywords=['voidtools', 'everything', 'efu'],

)
