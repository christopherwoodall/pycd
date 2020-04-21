#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;

""" pycd.py: Disassembler for Python Bytecode(pyc) files. """

__author__      = "Christopher Woodall"   #
__maintainer__  = "Christopher Woodall"   #
__license__     = ""                      #
__version__     = "0.0.1"                 #
__status__      = "Prototype"             # [ Prototype | Development | Production ]
__credits__     = [ ]


from pycd import *

import pprint
pp = pprint.PrettyPrinter( indent=2 )


test_file = './tests/Examples (python3).cpython-37.pyc'
disassembly = pycd.Disassembler( test_file )

#print( disassembly )
pp.pprint( disassembly.disassembly )


