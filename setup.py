#!/usr/bin/env python

from distutils.core import setup

setup(name='Pascal Compiler',
      version='1.0',
      description='Basic Pascal language compiler',
      author='Vinicius Barbosa Medeiros; Vinicius Misael Mendes de Moura',
      author_email='',
      url='https://github.com/bmviniciuss/ufpb-compiladores',
      packages=['compiler'],
      install_requires=['autopep8', 'pylint', 'pytest']
      )
