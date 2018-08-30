#!/usr/bin/env python

import sys
from DatabaseInterface import DatabaseInterface

x = DatabaseInterface( )
x.addPlayerToLeague( sys.argv[ 1 ], sys.argv[ 2 ] )
