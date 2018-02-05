#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='mblog',
    version='1.0',
    author='Yakovlev Andrey',
    author_email='679008@gmail.com',
    description='Parse MB logs',
    packages=find_packages(exclude=['tests']),
    url="http://facebook.com/",
    entry_points={
        'console_scripts': ['parse-log=mblog.command_line:main'],
    },
    install_requires=[
       'terminaltables',
        'colorclass'
    ]
)