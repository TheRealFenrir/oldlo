#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
print x.getPlayerHistory( int( sys.argv[ 1 ] ), int( sys.argv[ 2 ] ) )
