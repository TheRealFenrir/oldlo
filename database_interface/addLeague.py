#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
print x.addLeague( sys.argv[ 1 ] )
