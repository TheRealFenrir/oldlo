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

#league_id = form.getvalue( 'league_id' )
league_id = LEAGUE_ID;

print "Content-type:text/plain\n\n"
db = DatabaseInterface( )
print json.dumps( db.listPlayersInLeague( league_id ) )
