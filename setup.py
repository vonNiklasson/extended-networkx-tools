# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='extended_networkx_tools',
      version='0.7.4.rc1',
      description='Tools package for extending functionality of the networkx package.',
      keywords='graph distributed average consensus convergence rate',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/vonNiklasson/extended-networkx-tools',
      author='Johan Niklasson, Oskar Hahr',
      author_email='jnikl@kth.se, ohahr@kth.se',
      license='MIT',
      packages=find_packages(exclude=['twine']),
      install_requires=[
            'cycler',
            'decorator',
            'kiwisolver',
            'matplotlib',
            'networkx',
            'numpy',
            'pyparsing',
            'python-dateutil',
      ],
      py_modules=['six'],
      python_requires='~=3.0',
      zip_safe=False,
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',

            # Topics
            'Topic :: System :: Distributed Computing',
            'Topic :: Scientific/Engineering :: Mathematics',


            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
      ],
)
