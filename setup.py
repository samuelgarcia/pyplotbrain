#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os

install_requires = [ ]

setup(
    name = "pyplotbrain",
    version = '0.1dev',
    packages = ['pyplotbrain',],
    install_requires=install_requires,
    author = "Samuel Garcia",
    author_email = "sam.garcia.die@gmail.com",
    description = "Simple (and naive) tool to plot 3D glass brain in python",
    license = "BSD-3-Clause",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
        'Topic :: Scientific/Engineering']
)
