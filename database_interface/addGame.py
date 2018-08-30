#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
print x.addGame( int( sys.argv[ 1 ] ), int( sys.argv[ 2 ] ), int( sys.argv[ 3 ] ), int( sys.argv[ 4 ] ), int( sys.argv[ 5 ] ), int( sys.argv[ 6 ] ) )
