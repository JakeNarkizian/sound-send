
from distutils.core import setup
from setuptools import find_packages

setup(name='SoundSendServer',
      version='0.1',
      description='Python Backend Server for SoundSend App',
      author='Jake Narkizian, Sean Torres',
      packages=find_packages(where='src', exclude=['*.test.*']))
