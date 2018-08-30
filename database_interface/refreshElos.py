#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
print x.refreshElos( int( sys.argv[ 1 ] ) )
