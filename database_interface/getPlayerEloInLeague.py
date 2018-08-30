#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
print x.getPlayerEloInLeague( int( sys.argv[ 1 ] ), int( sys.argv[ 2 ] ) )
