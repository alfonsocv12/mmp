import os
import sys
import json

from mmp.cli.colors import bcolors
from setuptools import find_packages
from setuptools import setup


setup(
    name='mmp',
    version='0.0.2',
    authro='Alfonso Villaobos',
    author_email='alfonso@codepeat.com',
    url='https://github.com/alfonsocv12/mmp',
    license='MIT',
    description='MMP handle your py_modules easier and faster',
    packages=find_packages(exclude=['tests.*', 'tests']),
    long_description=open('readme.md', 'r').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['mmp=mmp.cli.main:main']
    },
    install_requires=[
        'virtualenv>=20.4.4',
        'docopt==0.6.2'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
