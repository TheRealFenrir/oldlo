#!/usr/bin/env python
#!/usr/bin/python

import cgi, cgitb 
import sys
import json
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'database_interface'))

from DatabaseInterface import DatabaseInterface
from constants import LEAGUE_ID

form = cgi.FieldStorage( ) 

p1_id = int( form.getvalue( 'p1_id' ) )
p2_id = int( form.getvalue( 'p2_id' ) )
p3_id = int( form.getvalue( 'p3_id' ) )
p4_id = int( form.getvalue( 'p4_id' ) )
#league_id = form.getvalue( 'league_id' )
league_id = LEAGUE_ID;

print "Content-type:text/plain\n\n"
db = DatabaseInterface( )
print json.dumps( db.getExpectedScore( p1_id, p2_id, p3_id, p4_id, league_id ) )
