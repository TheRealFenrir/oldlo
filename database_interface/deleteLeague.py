#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
x.deleteLeague( sys.argv[ 1 ] )
