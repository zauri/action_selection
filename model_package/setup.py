from setuptools import setup

setup(
   name='opportunistic_planning',
   version='1.0',
   description='Opportunistic sequence planning module',
   author='Petra Wenzl',
   packages=['opportunistic_planning'], 
   install_requires=['fastDamerauLevenshtein', 'pandas', 'numpy'],
)
