#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
print x.getLeagueHistory( int( sys.argv[ 1 ] ) )
