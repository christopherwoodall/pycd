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


import dis, importlib, inspect, marshal, opcode, os, re, struct, time, types
import io, contextlib


class Disassembler( object ):
  
  magic_number = importlib.util.MAGIC_NUMBER

  opcode_fields = (
    'opname',  # human readable name for operation
    'opcode',  # numeric code for operation
    'arg',     # numeric argument to operation (if any), otherwise None
    'argval',  # resolved arg value (if known), otherwise same as arg
    'argrepr',       # human readable description of operation argument
    'offset',        # start index of operation within bytecode sequence
    'starts_line',   # line started by this opcode (if any), otherwise None
    'is_jump_target' # True if other code jumps to here, otherwise False
  )

  metadata    = { }
  disassembly = { }

  
  @staticmethod
  def capture_std( callback, argv ):
    with contextlib.redirect_stdout( io.StringIO( ) ) as output:
      callback( argv )
    return output.getvalue( )


  def __init__( self, filename ):
    filename    = self.filename    = filename
    bytes       = self.bytes       = self.read( filename )
    code_object = self.code_object = self.load( bytes )
    metadata    = self.metadata    = self.meta_analysis( bytes[ :12 ], code_object )
    self.decompose( )


  def read( self, filename ):
    if not os.path.exists( filename ):
      raise IOError( 'ERROR: File does not exist!' )
    with open( filename, 'rb' ) as f:
      bytecode = f.read( )
      if bytecode[ :len( self.magic_number ) ] != self.magic_number:
        print( "Warning: Magic Number does not match!" )
    return bytecode


  def load( self, bytes ):
    return marshal.loads( bytes[ 16: ] )


  def meta_analysis( self, header, co ):
    compile_time = time.asctime( time.localtime(
      struct.unpack( 'L', header[ 8:12 ] )[ 0 ]
    ) )
    # TODO - 
    # dict( dis.findlinestarts( co ) )
    # 'line_starts':    [ lineno for offset, lineno in dis.findlinestarts( co ) ],
    # [ offset for offset, lineno in dis.findlinestarts( co ) ]
    # dis.findlabels( co.co_code )
    return {
      'filename':       co.co_filename,
      'compile_time':   compile_time,
      'flags':          co.co_flags,
      'stack_size':     co.co_stacksize,
      'first_line_no':  co.co_firstlineno,
      'kwargs_count':   co.co_kwonlyargcount,
      'argument_count': co.co_argcount,
      'local_count':    co.co_nlocals
    }


  def decompose( self ):
    co = self.code_object    
    self.walk( co )

    
  def walk( self, co, iteration=0 ):
    #if iteration is 0:
    self.analyze( co )

    consts = getattr( co, 'co_consts', None)
    if consts is not None:
      #print(consts )
      for const in consts:
        if isinstance( const, types.CodeType ):
          self.walk( const )


  def analyze( self, co ):
    # (1)|(2)|(3)|(4)|   (5)    |(6)|  (7)
    # ---|---|---|---|----------|---|-------
    # 1. Line number in source code
    # 2. Current instruction
    # 3. Possible jump
    # 4. Bytecode Address
    # 5. Instruction/Opname
    # 6. Internal python pointer to arguments on stack
    # 7. Human-Friendly interpertation
    disassembly = self.disassembly
    if isinstance( co, types.CodeType ):
      pydis = self.capture_std( dis.dis, co )  # dis.disassemble( co_code )
      lines = pydis.split( "\n\n" )
      for line in lines:
        if line.startswith( 'Disassembly of' ):
          line = "\n".join( line.split( "\n" )[ 1: ] )
        line_number = int( re.sub('[^0-9]+', '', line[ :9 ] ).strip( ) )
        disassembly[ line_number ] = line
 

# TODO
#def main( ):
#  pass
#if __name__ == "__main__":
  #main( sys.argv[1] )


"""
TODO
  o Check python version
     - Modify header layout based on(https://www.python.org/dev/peps/pep-0552/):
           i.   Python 2.0          8 Bytes
          ii.  Python 3.0 - 3.6   12 Bytes
         iii. Python 3.7         16 Bytes
     - Default Header Layout
          # Magic Numger   4 Bytes
          # Timestamp      4 Bytes
          # Marshal.dump( )
  o https://stackabuse.com/differences-between-pyc-pyd-and-pyo-python-files/
  o Return pesudo-code string
    #def __repr__( self ):
    # EXAMPLE - print( disassembly )
    #  return "TODO"
  o Class called as function
    #def __call__( self ):
    #  return "Called as function"   
"""


