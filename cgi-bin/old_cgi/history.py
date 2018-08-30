#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))

from DatabaseInterface import DatabaseInterface
import elo

db = DatabaseInterface( )

for game in db.history( ):
    print "(" + str( game[ 'p1_id' ] ) + ", " + str( game[ 'p2_id' ] ) + ") " + str( game[ 't1_score' ] ) + "-" + str( game[ 't2_score' ] ) + " (" + str( game[ 'p3_id' ] ) + ", " + str( game[ 'p4_id' ] ) + ")"
